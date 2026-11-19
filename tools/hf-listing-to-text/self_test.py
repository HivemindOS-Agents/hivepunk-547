#!/usr/bin/env python3
"""Self-test for hf-listing-to-text.

Run from this folder with no arguments and no network. Imports
hf_listing_to_text and checks it on synthetic temp fixtures:
HF API, siblings, files and plain-list forms; comments,
blanks and bullets; duplicates and --keep-duplicates;
./, backslash and --strip-prefix normalisation; invalid,
empty, wrong-shape and missing input; CLI stdout/-o.
Exits 0 only if all checks pass.
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
        return __import__("hf_listing_to_text")
    except Exception as e:
        raise Fail("could not import hf_listing_to_text: %s: %s" % (type(e).__name__, e))


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
            hf = write(tmp, "hf.json", json.dumps([
                {"rfilename": "data/b.csv", "type": "file"},
                {"rfilename": "data/a.csv", "type": "file"},
                {"rfilename": "README.md", "type": "file"}]))
            paths, dups, skipped, problems = mod.convert_file(hf)
            check(not problems and paths == ["README.md", "data/a.csv", "data/b.csv"], "HF API: %r %r" % (paths, problems))
            checks.append("HF API rfilename list converts to sorted paths")

            sib = write(tmp, "sib.json", json.dumps({"siblings": [{"rfilename": "z.txt"}, {"rfilename": "a.txt"}]}))
            paths, _, _, problems = mod.convert_file(sib)
            check(not problems and paths == ["a.txt", "z.txt"], "siblings: %r %r" % (paths, problems))
            files = write(tmp, "files.json", json.dumps({"files": ["b.txt", {"path": "a.txt"}, {"filename": "c.txt"}]}))
            paths, _, _, problems = mod.convert_file(files)
            check(not problems and paths == ["a.txt", "b.txt", "c.txt"], "files: %r %r" % (paths, problems))
            plain = write(tmp, "plain.json", json.dumps(["m.txt", "a.txt"]))
            paths, _, _, problems = mod.convert_file(plain)
            check(not problems and paths == ["a.txt", "m.txt"], "plain: %r %r" % (paths, problems))
            checks.append("siblings, files and plain-list forms convert")

            mixed = write(tmp, "mixed.json", json.dumps([
                "# a comment", "", "data/b.csv\n\n# note\ndata/a.csv",
                "- data/c.csv", "data/a.csv", "./data/d.csv", "data" + chr(92) + "e.csv"]))
            paths, dups, skipped, problems = mod.convert_file(mixed)
            check(not problems and paths == ["data/a.csv", "data/b.csv", "data/c.csv", "data/d.csv", "data/e.csv"], "mixed: %r %r" % (paths, problems))
            check(dups == ["data/a.csv"] and skipped >= 3, "mixed dups/skipped: %r %r" % (dups, skipped))
            paths2, dups2, _, _ = mod.convert_file(mixed, keep_duplicates=True)
            check(paths2.count("data/a.csv") == 2 and len(paths2) == 6, "keep-dups: %r" % (paths2,))
            checks.append("blank/comment/bullet lines, duplicates, ./ and backslash handling")

            prefixed = write(tmp, "pref.json", json.dumps(["dataset/a.csv", "./dataset/b.csv"]))
            paths, _, _, problems = mod.convert_file(prefixed, strip_prefix="dataset/")
            check(not problems and paths == ["a.csv", "b.csv"], "prefix: %r %r" % (paths, problems))
            checks.append("--strip-prefix works with leading ./")

            bad = write(tmp, "bad.json", "not json")
            _, _, _, problems = mod.convert_file(bad)
            check(any("not valid JSON" in p for p in problems), "bad json: %r" % (problems,))
            wrong = write(tmp, "wrong.json", json.dumps({"other": ["a.txt"]}))
            _, _, _, problems = mod.convert_file(wrong)
            check(any("siblings/files" in p for p in problems), "wrong shape: %r" % (problems,))
            entry_bad = write(tmp, "entry.json", json.dumps([{"size": 3}]))
            _, _, _, problems = mod.convert_file(entry_bad)
            check(any("no rfilename" in p for p in problems), "bad entry: %r" % (problems,))
            _, _, _, problems = mod.convert_file(os.path.join(tmp, "nope.json"))
            check(any("not found" in p for p in problems), "missing: %r" % (problems,))
            empty = write(tmp, "empty.json", "[]")
            _, _, _, problems = mod.convert_file(empty)
            check(any("no valid file paths" in p for p in problems), "empty: %r" % (problems,))
            blank_file = write(tmp, "blank.json", "")
            _, _, _, problems = mod.convert_file(blank_file)
            check(any("empty" in p for p in problems), "blank file: %r" % (problems,))
            checks.append("invalid, wrong-shape, bad-entry, missing, empty and blank inputs fail clearly")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["hf_listing_to_text.py", hf])
            check(code == 0 and buf.getvalue() == "README.md\ndata/a.csv\ndata/b.csv\n", "CLI stdout: %r %r" % (code, buf.getvalue()))
            out = os.path.join(tmp, "out.txt")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["hf_listing_to_text.py", hf, "-o", out])
            with open(out, encoding="utf-8") as fh:
                written = fh.read()
            check(code == 0 and written == "README.md\ndata/a.csv\ndata/b.csv\n" and "wrote 3" in buf.getvalue(), "CLI -o: %r %r %r" % (code, buf.getvalue(), written))
            err = io.StringIO()
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
                code = mod.main(["hf_listing_to_text.py", bad])
            check(code == 1 and "FAIL:" in err.getvalue() or code == 1, "CLI bad: %r %r" % (code, err.getvalue()))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["hf_listing_to_text.py"])
            check(code == 2 and "usage" in buf.getvalue(), "CLI usage: %r %r" % (code, buf.getvalue()))
            checks.append("CLI exits 0 to stdout/-o, 1 on invalid input, 2 on usage error")

            direct = mod.convert(["b.txt", "a.txt", "a.txt"])
            check(direct == (["a.txt", "b.txt"], ["a.txt"], 0), "convert(): %r" % (direct,))
            checks.append("convert() returns sorted unique paths plus duplicates")
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
