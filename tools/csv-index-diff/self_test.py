#!/usr/bin/env python3
"""Self-test for csv-index-diff.

Run from this folder with no arguments and no network. Imports
csv_index_diff, then checks it on synthetic CSVs in a temp
directory: identical, changed, added/removed, and duplicate
cases, plus missing-file and bad-header failures and CLI exit
codes. Exits 0 only if all checks pass.
"""

import contextlib
import io
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HEADER = "file_name,bytes,lines\n"


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
        return __import__("csv_index_diff")
    except Exception as e:
        raise Fail("could not import csv_index_diff: %s: %s" % (type(e).__name__, e))


def write(folder, name, text):
    path = os.path.join(folder, name)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    return path


def main():
    try:
        mod = import_tool()
        checks = []
        with tempfile.TemporaryDirectory() as tmp:
            base = HEADER + "alpha.py,10,2\nbeta.txt,5,1\n"
            old = write(tmp, "old.csv", base)
            same = write(tmp, "same.csv", base)
            ok, lines = mod.diff_files(old, same)
            check(ok and lines == [], "identical: ok=%r lines=%r" % (ok, lines))
            checks.append("identical case passes with no differences")

            changed = write(tmp, "changed.csv", HEADER + "alpha.py,12,2\nbeta.txt,5,3\n")
            ok, lines = mod.diff_files(old, changed)
            joined = " ".join(lines)
            check(not ok, "changed case should fail")
            check("changed: alpha.py" in joined and "changed: beta.txt" in joined, "changed lines %r" % (lines,))
            check("old bytes=10" in joined and "new bytes=12" in joined, "changed detail %r" % (lines,))
            checks.append("changed case reports alpha.py and beta.txt with old/new values")

            moved = write(tmp, "moved.csv", HEADER + "alpha.py,10,2\ngamma.txt,7,4\n")
            ok, lines = mod.diff_files(old, moved)
            joined = " ".join(lines)
            check(not ok, "added/removed case should fail")
            check("added: gamma.txt" in joined, "added line %r" % (lines,))
            check("removed: beta.txt" in joined, "removed line %r" % (lines,))
            checks.append("added/removed case reports added gamma.txt and removed beta.txt")

            dup = write(tmp, "dup.csv", HEADER + "alpha.py,10,2\nalpha.py,10,2\nbeta.txt,5,1\n")
            ok, lines = mod.diff_files(old, dup)
            joined = " ".join(lines)
            check(not ok and "duplicate" in joined and "alpha.py" in joined and "new" in joined, "dup lines %r" % (lines,))
            ok2, lines2 = mod.diff_files(dup, same)
            check(not ok2 and "duplicate" in " ".join(lines2) and "old" in " ".join(lines2), "dup-old lines %r" % (lines2,))
            checks.append("duplicate case fails and names alpha.py in new and in old")

            empty_old = write(tmp, "empty_old.csv", HEADER)
            ok, lines = mod.diff_files(empty_old, moved)
            check(not ok and "added: alpha.py" in " ".join(lines), "empty-old %r" % (lines,))
            checks.append("header-only old file reports every new row as added")

            ok, lines = mod.diff_files(os.path.join(tmp, "missing.csv"), old)
            check(not ok and any("not found" in l for l in lines), "missing file %r" % (lines,))
            bad = write(tmp, "bad.csv", "name,size\nalpha.py,10\n")
            ok, lines = mod.diff_files(old, bad)
            check(not ok and any("bad header" in l for l in lines), "bad header %r" % (lines,))
            checks.append("missing file and bad header fail with clear messages")

            unsorted = write(tmp, "unsorted.csv", HEADER + "beta.txt,5,1\nalpha.py,10,2\n")
            ok, lines = mod.diff_files(old, unsorted)
            check(not ok and any("not sorted" in l for l in lines), "unsorted %r" % (lines,))
            checks.append("unsorted rows fail and are reported")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["csv_index_diff.py", old, same])
            check(code == 0 and buf.getvalue().startswith("ok:"), "CLI identical %r %r" % (code, buf.getvalue()))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["csv_index_diff.py", old, changed])
            check(code == 1 and "FAIL:" in buf.getvalue(), "CLI changed %r %r" % (code, buf.getvalue()))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["csv_index_diff.py", old])
            check(code == 1 and "usage" in buf.getvalue(), "CLI usage %r %r" % (code, buf.getvalue()))
            checks.append("CLI exits 0 for identical, 1 with FAIL for changed and for bad usage")
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
