#!/usr/bin/env python3
"""Self-test for dataset-manifest-check.

Run from this folder with no arguments and no network. Imports
dataset_manifest_check, then checks it on synthetic fixtures in a
temp directory: valid text/JSON/CSV manifests, missing listed
files, unlisted files, empty manifest, unsafe paths, missing
manifest, and CLI exit codes. Exits 0 only if all checks pass.
"""

import contextlib
import io
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


class Fail(Exception):
    pass


def check(cond, msg):
    if not cond:
        raise Fail(msg)


def import_tool():
    sys.dont_write_bytecode = True
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    try:
        return __import__("dataset_manifest_check")
    except Exception as e:
        raise Fail("could not import dataset_manifest_check: %s: %s" % (type(e).__name__, e))


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    return path


def main():
    try:
        mod = import_tool()
        checks = []
        with tempfile.TemporaryDirectory() as tmp:
            data = os.path.join(tmp, "data")
            os.makedirs(data)
            write(data, "a.txt", "alpha\n")
            write(data, "sub/b.csv", "x,y\n1,2\n")
            write(data, "sub/c.json", "{\"k\": 1}\n")

            manifest = write(data, "manifest.txt", "# dataset files\na.txt\nsub/b.csv\nsub/c.json\n")
            ok, problems, notes, counts = mod.check(manifest)
            check(ok and problems == [] and counts == {"listed": 3, "present": 3, "missing": 0, "unlisted": 0}, "valid text: %r %r" % (problems, counts))
            checks.append("valid text manifest passes with counts 3/3/0/0")

            text_entries = mod.parse_manifest(manifest)
            check(text_entries == ["a.txt", "sub/b.csv", "sub/c.json"], "text parse: %r" % (text_entries,))
            checks.append("text parser ignores comment and keeps order")

            json_manifest = write(data, "manifest.json", json.dumps({"files": ["a.txt", {"path": "sub/b.csv"}, {"name": "sub/c.json"}]}))
            ok, problems, notes, counts = mod.check(json_manifest)
            check(ok and counts["listed"] == 3 and counts["present"] == 3, "valid json: %r %r" % (problems, counts))
            checks.append("valid JSON manifest (strings and objects) passes")

            csv_manifest = write(data, "manifest.csv", "name,bytes\na.txt,5\nsub/b.csv,3\nsub/c.json,8\n")
            ok, problems, notes, counts = mod.check(csv_manifest)
            check(ok and counts["listed"] == 3 and counts["present"] == 3, "valid csv: %r %r" % (problems, counts))
            checks.append("valid CSV manifest passes using name column")

            missing = write(data, "bad_missing.txt", "a.txt\nsub/nope.txt\n")
            ok, problems, notes, counts = mod.check(missing)
            joined = " ".join(problems)
            check(not ok and counts["missing"] == 1 and "listed file not found: sub/nope.txt" in joined, "missing: %r %r" % (problems, counts))
            checks.append("missing listed file fails naming sub/nope.txt")

            unlisted = write(data, "bad_unlisted.txt", "a.txt\n")
            ok, problems, notes, counts = mod.check(unlisted)
            joined = " ".join(problems)
            check(not ok and counts["unlisted"] >= 2 and "unlisted file: sub/b.csv" in joined and "unlisted file: sub/c.json" in joined, "unlisted: %r %r" % (problems, counts))
            check(notes == [] or all("unlisted" not in n for n in notes), "unlisted notes: %r" % (notes,))
            checks.append("unlisted files are flagged and fail")

            ok2, problems2, notes2, counts2 = mod.check(unlisted, allow_unlisted=True)
            check(ok2 and any("unlisted file: sub/b.csv" in n for n in notes2), "allow-unlisted: %r %r" % (problems2, notes2))
            checks.append("--allow-unlisted reports unlisted as NOTE and passes")

            empty = write(data, "empty.txt", "# nothing here\n")
            ok, problems, notes, counts = mod.check(empty)
            check(not ok and any("lists no files" in p for p in problems), "empty: %r" % (problems,))
            checks.append("empty manifest fails with lists-no-files")

            unsafe = write(data, "unsafe.txt", "../secret.txt\n/abs/path.txt\n")
            ok, problems, notes, counts = mod.check(unsafe)
            joined = " ".join(problems)
            check(not ok and counts["missing"] == 2 and joined.count("escapes root") == 2, "unsafe: %r" % (problems,))
            checks.append("unsafe ../ and absolute paths are rejected")

            ok, problems, notes, counts = mod.check(os.path.join(data, "nope.txt"))
            check(not ok and any("manifest not found" in p for p in problems), "missing manifest: %r" % (problems,))
            checks.append("missing manifest fails with not found")

            dup = write(data, "dup.txt", "a.txt\na.txt\nsub/b.csv\nsub/c.json\n")
            ok, problems, notes, counts = mod.check(dup)
            check(ok and counts["listed"] == 4 and counts["present"] == 3, "dup: %r %r" % (problems, counts))
            check(any("duplicate" in n for n in notes), "dup notes: %r" % (notes,))
            checks.append("duplicate entry checked once with NOTE")

            other_root = os.path.join(tmp, "elsewhere")
            os.makedirs(other_root)
            write(other_root, "a.txt", "x\n")
            ok, problems, notes, counts = mod.check(manifest, root=other_root)
            check(not ok and counts["missing"] == 2, "other root: %r %r" % (problems, counts))
            checks.append("--root override checks against the other folder")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["dataset_manifest_check.py", manifest])
            out = buf.getvalue()
            check(code == 0 and "PASS:" in out and "listed: 3" in out, "CLI valid: %r %r" % (code, out))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["dataset_manifest_check.py", missing])
            out = buf.getvalue()
            check(code == 1 and "FAIL:" in out and "missing: 1" in out, "CLI fail: %r %r" % (code, out))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["dataset_manifest_check.py", unlisted, "--allow-unlisted"])
            check(code == 0 and "NOTE:" in buf.getvalue(), "CLI allow: %r %r" % (code, buf.getvalue()))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["dataset_manifest_check.py"])
            check(code == 1 and "usage" in buf.getvalue(), "CLI no args: %r %r" % (code, buf.getvalue()))
            checks.append("CLI exits 0 with PASS, 1 with FAIL, handles flags and no args")
    except Fail as e:
        sys.stderr.write("FAIL: %s\n" % e)
        return 1
    except Exception as e:
        sys.stderr.write("FAIL: unexpected %s: %s\n" % (type(e).__name__, e))
        return 1
    for line in checks:
        print(line)
    print("self-test: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
