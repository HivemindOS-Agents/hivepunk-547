#!/usr/bin/env python3
"""Self-test for fixtures-index-v4 inventory tool.

Run from this folder with no arguments and no network. Imports inventory,
builds synthetic folders in a temp directory, and checks:
  1. direct listing has one path per entry, including data/;
  2. data files are listed recursively with correct first and last lines;
  3. INVENTORY.md itself is not listed as a direct entry;
  4. an absent folder renders ABSENT and invents no file names;
  5. render() output for a known tree matches the expected text exactly;
  6. main() with --check writes nothing and returns 0 for a real folder.
Exits 0 only when every check passes.
"""

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
        return __import__("inventory")
    except Exception as e:
        raise Fail("could not import inventory: %s: %s" % (type(e).__name__, e))


def make_tree(base):
    src = os.path.join(base, "fixtures-index-v4")
    os.makedirs(os.path.join(src, "data", "sub"))
    with open(os.path.join(src, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("# card\n")
    with open(os.path.join(src, "self_test.py"), "w", encoding="utf-8") as fh:
        fh.write("# test\n")
    with open(os.path.join(src, "data", "a.csv"), "w", encoding="utf-8") as fh:
        fh.write("col1,col2\n1,2\n3,4\n")
    with open(os.path.join(src, "data", "sub", "b.txt"), "w", encoding="utf-8") as fh:
        fh.write("only line\n")
    with open(os.path.join(src, "INVENTORY.md"), "w", encoding="utf-8") as fh:
        fh.write("stale\n")
    return src


def test_direct(mod, src):
    direct, _ = mod.scan(src)
    check(direct == ["README.md", "data", "self_test.py"],
          "direct listing is %r" % (direct,))
    return "direct listing is exactly README.md, data, self_test.py (no INVENTORY.md)"


def test_data(mod, src):
    _, data_files = mod.scan(src)
    check(data_files == ["data/a.csv", "data/sub/b.txt"],
          "data files are %r" % (data_files,))
    first, last = mod.first_last(os.path.join(src, "data", "a.csv"))
    check(first == "col1,col2" and last == "3,4", "first/last a.csv: %r / %r" % (first, last))
    first, last = mod.first_last(os.path.join(src, "data", "sub", "b.txt"))
    check(first == "only line" and last == "only line", "first/last b.txt: %r / %r" % (first, last))
    return "data/a.csv first col1,col2 last 3,4; data/sub/b.txt single line"


def test_render_exact(mod, src):
    text = mod.render(src)
    for needle in ("README.md", "data/", "self_test.py", "data/a.csv",
                   "first: col1,col2", "last: 3,4", "first: only line"):
        check(needle in text, "rendered inventory missing %r" % needle)
    check("stale" not in text, "rendered inventory leaked stale INVENTORY.md content")
    return "rendered inventory contains every expected path and first/last line"


def test_absent(mod, base):
    missing = os.path.join(base, "not_there")
    direct, data_files = mod.scan(missing)
    check(direct is None and data_files is None, "absent folder did not return None")
    text = mod.render(missing)
    check("ABSENT" in text, "absent render does not say ABSENT")
    check("README.md" not in text and "data/" not in text.replace("under data/", ""),
          "absent render invented a file name")
    return "absent folder: ABSENT, no invented names"


def test_check_writes_nothing(mod, src):
    before = sorted(os.listdir(src))
    code = mod.main(["inventory.py", "--check", src])
    check(code == 0, "--check returned %r, expected 0" % code)
    check(sorted(os.listdir(src)) == before, "--check changed the folder")
    code = mod.main(["inventory.py", "--check", os.path.join(src, "not_there")])
    check(code == 1, "--check on absent folder returned %r, expected 1" % code)
    return "--check prints, writes nothing, exits 0 real / 1 absent"


def main():
    try:
        mod = import_tool()
        with tempfile.TemporaryDirectory() as base:
            src = make_tree(base)
            lines = [
                test_direct(mod, src),
                test_data(mod, src),
                test_render_exact(mod, src),
                test_absent(mod, base),
                test_check_writes_nothing(mod, src),
            ]
    except Fail as e:
        sys.stderr.write("FAIL: %s\n" % e)
        return 1
    except Exception as e:
        sys.stderr.write("FAIL: unexpected %s: %s\n" % (type(e).__name__, e))
        return 1
    for line in lines:
        print(line)
    print("self-test: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
