#!/usr/bin/env python3
"""Self-test for fixtures-index-v4.

Run from this folder with no arguments and no network. Imports
index, then checks it on synthetic fixture folders in a temp
directory: a normal folder, an empty directory, a folder with a
binary file (blank lines, exact byte size), and sorting of names.
Also checks the missing-path and not-a-directory failures and CLI
exit codes. Exits 0 only if all checks pass.
"""

import contextlib
import io
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
        return __import__("index")
    except Exception as e:
        raise Fail("could not import index: %s: %s" % (type(e).__name__, e))


def write(folder, name, data):
    path = os.path.join(folder, name)
    mode = "wb" if isinstance(data, bytes) else "w"
    with open(path, mode) as fh:
        fh.write(data)
    return path


def rows_by_name(rows):
    return {r[0]: r for r in rows}


def main():
    try:
        mod = import_tool()
        checks = []

        with tempfile.TemporaryDirectory() as tmp:
            normal = os.path.join(tmp, "normal")
            os.mkdir(normal)
            write(normal, "a.py", "one\ntwo\nthree\n")
            write(normal, "b.md", "# title\n\nbody")
            write(normal, "c.txt", "")
            write(normal, "d.json", '{"a": 1}\n')
            write(normal, "e.csv", "x,y\n1,2\n")
            sub = os.path.join(normal, "sub")
            os.mkdir(sub)
            write(sub, "inner.py", "hidden\n")
            ok, problems, rows = mod.verify(normal)
            check(ok, "normal fixture failed: %r" % (problems,))
            check([r[0] for r in rows] == ["a.py", "b.md", "c.txt", "d.json", "e.csv"],
                  "normal rows are %r" % (rows,))
            by = rows_by_name(rows)
            check(by["a.py"][2] == 3, "a.py lines are %r" % (by["a.py"],))
            check(by["b.md"][2] == 3, "b.md lines (no trailing newline) are %r" % (by["b.md"],))
            check(by["c.txt"][2] == 0, "c.txt lines are %r" % (by["c.txt"],))
            check(by["d.json"][2] == 1, "d.json lines are %r" % (by["d.json"],))
            check(by["e.csv"][2] == 2, "e.csv lines are %r" % (by["e.csv"],))
            check(by["a.py"][1] == len("one\ntwo\nthree\n"), "a.py bytes are %r" % (by["a.py"],))
            check(all(r[0] != "inner.py" for r in rows), "subdirectory file was indexed")
            checks.append("normal fixture: sizes and line counts correct, subdirectory skipped")

            empty = os.path.join(tmp, "empty")
            os.mkdir(empty)
            ok, problems, rows = mod.verify(empty)
            check(ok and rows == [], "empty dir: %r %r" % (problems, rows))
            check(mod.render_csv(rows) == "file_name,bytes,lines\n",
                  "empty CSV is %r" % (mod.render_csv(rows),))
            checks.append("empty directory yields header only")

            binary = os.path.join(tmp, "binary")
            os.mkdir(binary)
            payload = bytes(range(256)) * 4
            write(binary, "blob.bin", payload)
            write(binary, "UPPER.PY", "x\ny\n")
            ok, problems, rows = mod.verify(binary)
            check(ok, "binary fixture failed: %r" % (problems,))
            by = rows_by_name(rows)
            check(by["blob.bin"][1] == len(payload), "blob.bin bytes are %r" % (by["blob.bin"],))
            check(by["blob.bin"][2] is None, "blob.bin lines should be blank: %r" % (by["blob.bin"],))
            check(by["UPPER.PY"][2] == 2, "UPPER.PY lines are %r" % (by["UPPER.PY"],))
            check("blob.bin,%d,\n" % len(payload) in mod.render_csv(rows),
                  "binary CSV row missing: %r" % (mod.render_csv(rows),))
            checks.append("binary-size fixture: exact bytes, blank lines, uppercase extension counted")

            sorting = os.path.join(tmp, "sorting")
            os.mkdir(sorting)
            for name in ["zebra.txt", "apple.txt", "Mango.txt", "banana.txt"]:
                write(sorting, name, "x\n")
            ok, problems, rows = mod.verify(sorting)
            check(ok, "sorting fixture failed: %r" % (problems,))
            names = [r[0] for r in rows]
            check(names == sorted(names), "rows not sorted: %r" % (names,))
            check(names == ["Mango.txt", "apple.txt", "banana.txt", "zebra.txt"],
                  "sorted names are %r" % (names,))
            checks.append("sorting fixture: rows sorted by file_name")

            ok, problems, rows = mod.verify(os.path.join(tmp, "missing"))
            check(not ok and any("not found" in p for p in problems), "missing path: %r" % (problems,))
            not_dir = write(tmp, "afile.txt", "x\n")
            ok, problems, rows = mod.verify(not_dir)
            check(not ok and any("not a directory" in p for p in problems), "not a directory: %r" % (problems,))
            checks.append("missing path and not-a-directory fail with clear messages")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["index.py", normal])
            check(code == 0 and buf.getvalue().startswith("file_name,bytes,lines\n"),
                  "CLI good %r %r" % (code, buf.getvalue()))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["index.py", os.path.join(tmp, "missing")])
            check(code == 1 and "FAIL:" in buf.getvalue(), "CLI bad %r %r" % (code, buf.getvalue()))
            checks.append("CLI exits 0 with CSV for good dir and 1 with FAIL for missing dir")
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
