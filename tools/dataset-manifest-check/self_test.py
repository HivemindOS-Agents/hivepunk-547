#!/usr/bin/env python3
"""Self-test for dataset-manifest-check (manifest vs listing).

Run from this folder with no arguments and no network. Imports
dataset_manifest_check, then checks it on synthetic fixtures in
a temp directory: exact match, missing/extra files, duplicates
on each side, object-form manifest, listing comments/bullets,
./ and prefix normalisation, empty/invalid/missing inputs, and
CLI exit codes. Exits 0 only if all checks pass.
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


def write(root, name, text):
    path = os.path.join(root, name)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    return path


def main():
    try:
        mod = import_tool()
        checks = []
        with tempfile.TemporaryDirectory() as tmp:
            manifest = write(tmp, "manifest.json", json.dumps(["data/a.csv", "data/b.csv", "README.md"]))
            listing = write(tmp, "listing.txt", "# public listing\n\ndata/a.csv\n- data/b.csv\n* README.md\n")
            ok, result, problems, notes = mod.check(manifest, listing)
            check(ok and result["common"] == 3 and result["manifest_count"] == 3 and result["listing_count"] == 3, "exact: %r %r" % (problems, result))
            checks.append("exact sets pass (comments, blank lines and bullets handled)")

            manifest2 = write(tmp, "m2.json", json.dumps({"files": [{"path": "data/a.csv"}, {"file": "data/missing.csv"}]}))
            listing2 = write(tmp, "l2.txt", "data/a.csv\ndata/extra.txt\n")
            ok, result, problems, notes = mod.check(manifest2, listing2)
            check(not ok and result["only_in_manifest"] == ["data/missing.csv"] and result["only_in_listing"] == ["data/extra.txt"] and result["common"] == 1, "diff: %r %r" % (problems, result))
            checks.append("object-form manifest: missing/extra reported sorted, common counted")

            dup_m = write(tmp, "dupm.json", json.dumps(["a.txt", "a.txt", "b.txt"]))
            dup_l = write(tmp, "dupl.txt", "a.txt\nb.txt\nb.txt\n")
            ok, result, problems, notes = mod.check(dup_m, dup_l)
            check(not ok and result["duplicates_in_manifest"] == ["a.txt"] and result["duplicates_in_listing"] == ["b.txt"] and result["common"] == 2, "dups: %r %r" % (problems, result))
            checks.append("duplicates on either side fail and name the entry")

            prefixed_m = write(tmp, "pm.json", json.dumps(["dataset/a.csv", "dataset/b.csv"]))
            prefixed_l = write(tmp, "pl.txt", "./dataset/a.csv\ndataset/b.csv\n")
            ok, result, problems, notes = mod.check(prefixed_m, prefixed_l, strip_prefix="dataset/")
            check(ok and result["common"] == 2, "prefix: %r %r" % (problems, result))
            ok2, result2, _, _ = mod.check(prefixed_m, prefixed_l)
            check(ok2, "leading ./ alone should also match: %r" % (result2,))
            checks.append("--strip-prefix and leading ./ normalisation work")

            empty_m = write(tmp, "empty.json", "[]")
            ok, result, problems, notes = mod.check(empty_m, listing)
            check(not ok and any("lists no files" in p for p in problems), "empty manifest: %r" % (problems,))
            checks.append("empty manifest fails")

            bad = write(tmp, "bad.json", "not json")
            ok, result, problems, notes = mod.check(bad, listing)
            check(not ok and any("not valid JSON" in p for p in problems), "bad json: %r" % (problems,))
            checks.append("invalid JSON manifest fails")

            ok, result, problems, notes = mod.check(os.path.join(tmp, "nope.json"), listing)
            check(not ok and any("not found" in p for p in problems), "missing manifest: %r" % (problems,))
            ok, result, problems, notes = mod.check(manifest, os.path.join(tmp, "nope.txt"))
            check(not ok and any("not found" in p for p in problems), "missing listing: %r" % (problems,))
            checks.append("missing manifest or listing fails with not found")

            direct = mod.compare(["x.txt", "y.txt"], ["y.txt", "z.txt"])
            check(direct["only_in_manifest"] == ["x.txt"] and direct["only_in_listing"] == ["z.txt"] and not direct["ok"], "compare(): %r" % (direct,))
            checks.append("compare() returns exact set differences")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["dataset_manifest_check.py", manifest, listing])
            out = buf.getvalue()
            check(code == 0 and "PASS:" in out and "common: 3" in out, "CLI pass: %r %r" % (code, out))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["dataset_manifest_check.py", manifest2, listing2])
            out = buf.getvalue()
            check(code == 1 and "FAIL:" in out and "only in manifest: data/missing.csv" in out and "only in listing: data/extra.txt" in out, "CLI fail: %r %r" % (code, out))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["dataset_manifest_check.py", manifest + ","]) if False else mod.main(["dataset_manifest_check.py"])
            check(code == 2 and "usage" in buf.getvalue(), "CLI usage: %r %r" % (code, buf.getvalue()))
            checks.append("CLI exits 0 with PASS, 1 with FAIL, 2 on usage error")
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
