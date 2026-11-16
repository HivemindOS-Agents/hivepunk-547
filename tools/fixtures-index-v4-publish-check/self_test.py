#!/usr/bin/env python3
"""Self-test for fixtures-index-v4-publish-check.

Run from this folder with no arguments and no network. Imports
check_package, checks the included data.csv passes, then checks
synthetic CSVs in a temp directory: 3 rows, 5 rows, duplicate file_name,
missing column, extra column, empty description, and a source_url outside
tools/fixtures-index-v4. Exits 0 only when every check passes.
"""

import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HEADER = "file_name,source_url,description\n"
BASE = "https://github.com/HivemindOS-Agents/hivepunk-547/blob/main/tools/fixtures-index-v4/"
GOOD_ROWS = [
    ("inventory.py", "Builds INVENTORY.md by listing the folder"),
    ("self_test.py", "Self-test for the inventory tool"),
    ("README.md", "User guide for the inventory tool"),
    ("INVENTORY.md", "Inventory record for the folder"),
]


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
        return __import__("check_package")
    except Exception as e:
        raise Fail("could not import check_package: %s: %s"
                   % (type(e).__name__, e))


def make_csv(folder, name, text):
    path = os.path.join(folder, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def row(name, desc, url=None):
    return "%s,%s,%s\n" % (name, url if url is not None else BASE + name, desc)


def good_text(rows=None):
    rows = GOOD_ROWS if rows is None else rows
    return HEADER + "".join(row(n, d) for n, d in rows)


def main():
    try:
        mod = import_tool()
        checks = []

        ok, problems, names = mod.verify(os.path.join(HERE, "data.csv"))
        expected = [n for n, _ in GOOD_ROWS]
        check(ok, "included data.csv failed: %r" % (problems,))
        check(names == expected, "included data.csv names are %r" % (names,))
        checks.append("included data.csv passes: 4 unique rows (%s)"
                      % ", ".join(names))

        with tempfile.TemporaryDirectory() as tmp:
            path = make_csv(tmp, "good.csv", good_text())
            ok, problems, _ = mod.verify(path)
            check(ok, "synthetic good CSV failed: %r" % (problems,))
            checks.append("synthetic good CSV (4 rows) passes")

            cases = []
            cases.append(("3 rows", good_text(GOOD_ROWS[:3]), "row count is 3"))
            five = GOOD_ROWS + [("extra.py", "Extra row that should not be there")]
            cases.append(("5 rows", good_text(five), "row count is 5"))
            dup = [GOOD_ROWS[0], GOOD_ROWS[0], GOOD_ROWS[2], GOOD_ROWS[3]]
            cases.append(("duplicate", good_text(dup), "duplicate"))
            no_desc_header = "file_name,source_url\n" + "".join(
                "%s,%s\n" % (n, BASE + n) for n, _ in GOOD_ROWS)
            cases.append(("missing column", no_desc_header, "header is"))
            extra = "file_name,source_url,description,extra\n" + "".join(
                row(n, d).rstrip("\n") + ",x\n" for n, d in GOOD_ROWS)
            cases.append(("extra column", extra, "header is"))
            empty = GOOD_ROWS[:3] + [("INVENTORY.md", "")]
            cases.append(("empty description", good_text(empty), "empty description"))
            outside = HEADER + "".join(row(n, d) for n, d in GOOD_ROWS[:3])
            outside += row("INVENTORY.md", "Desc",
                           url="https://example.com/tools/other/INVENTORY.md")
            cases.append(("url outside path", outside, "is not under"))
            wrong_tail = HEADER + "".join(row(n, d) for n, d in GOOD_ROWS[:3])
            wrong_tail += row("INVENTORY.md", "Desc", url=BASE + "OTHER.md")
            cases.append(("url tail mismatch", wrong_tail, "expected"))

            for label, text, needle in cases:
                path = make_csv(tmp, label.replace(" ", "_") + ".csv", text)
                ok, problems, _ = mod.verify(path)
                check(not ok, "%s unexpectedly passed" % label)
                check(any(needle in p for p in problems),
                      "%s problems %r do not mention %r" % (label, problems, needle))
                checks.append("%s fails and mentions %r" % (label, needle))

            ok, problems, _ = mod.verify(os.path.join(tmp, "missing.csv"))
            check(not ok and any("not found" in p for p in problems),
                  "missing file: %r" % (problems,))
            checks.append("missing file fails with 'not found'")

            code = mod.main(["check_package.py", make_csv(tmp, "cli.csv", good_text())])
            check(code == 0, "CLI good returned %r" % code)
            code = mod.main(["check_package.py", make_csv(tmp, "cli_bad.csv", good_text(GOOD_ROWS[:2]))])
            check(code == 1, "CLI bad returned %r" % code)
            checks.append("CLI exits 0 for good CSV and 1 for bad CSV")
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
