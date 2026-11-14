#!/usr/bin/env python3
"""Top-of-folder self-test for agent-memory-lint-fixtures-index-v4.

Run with no arguments, from this folder. No network, no writes. Exits 0 only
when every check passes.

It imports the tool's own code (index_check.parse_markdown, index_check.compare)
and runs it on bundled sample data:

  * clean sample of three entries and three matching rows -> 0 issues
  * broken sample: three JSON entries, a two-row table and mutated values
    -> exactly four issues, asserted one by one
  * this folder's own index.json + index.md pair -> 0 issues, and the
    fixtures named in the index are present on disk

The readback-only checks live in readback.py and are exercised via readback.py's
--offline sample path; they are skipped here so this test imports only code that
is present in the shipped five files.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

CLEAN_JSON = {
    "entries": [
        {"path": "fixtures/clean/", "rule": "no findings on a clean fixture", "expected_exit_code": 0},
        {"path": "fixtures/bad-rows/", "rule": "row count or empty-cell finding", "expected_exit_code": 1},
        {"path": "fixtures/bad-card/", "rule": "missing closing 'What could not be checked' section", "expected_exit_code": 1},
    ]
}

CLEAN_MD = (
    "# sample\n\n"
    "| Path | Rule | Expected exit code |\n"
    "|---|---|---|\n"
    "| `fixtures/clean/` | no findings on a clean fixture | 0 |\n"
    "| `fixtures/bad-rows/` | row count or empty-cell finding | 1 |\n"
    "| `fixtures/bad-card/` | missing closing 'What could not be checked' section | 1 |\n"
)

BROKEN_JSON = {
    "entries": [
        {"path": "fixtures/clean/", "rule": "no findings on a clean fixture", "expected_exit_code": 0},
        {"path": "fixtures/bad-rows/", "rule": "row count or empty-cell finding", "expected_exit_code": 1},
        {"path": "fixtures/bad-card/", "rule": "missing closing 'What could not be checked' section", "expected_exit_code": 1},
    ]
}

# Two rows: bad-card row missing, clean row's rule mutated, bad-rows code flipped.
BROKEN_MD = (
    "| Path | Rule | Expected exit code |\n"
    "|---|---|---|\n"
    "| `fixtures/clean/` | findings are expected everywhere | 0 |\n"
    "| `fixtures/bad-rows/` | row count or empty-cell finding | 0 |\n"
)

EXPECTED_BROKEN = [
    "count mismatch: index has 3 entries, markdown has 2 rows",
    "entry 'fixtures/bad-card/' in index but not in markdown",
    "row 'fixtures/clean/': rule differs: markdown='findings are expected everywhere' index='no findings on a clean fixture'",
    "row 'fixtures/bad-rows/': expected_exit_code differs: index=1 markdown=0",
]


class Fail(Exception):
    pass


def check(cond, msg):
    if not cond:
        raise Fail(msg)


def import_tool(name):
    sys.dont_write_bytecode = True
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    return __import__(name)


def test_clean(mod):
    rows = mod.parse_markdown(CLEAN_MD)
    check(len(rows) == 3, "clean sample: parsed %d rows, expected 3" % len(rows))
    issues = mod.compare(CLEAN_JSON, rows, folders=None, base=HERE)
    check(issues == [], "clean sample: expected 0 issues, got %r" % issues)
    return "clean sample: 3 row(s), 0 issue(s)"


def test_broken(mod):
    rows = mod.parse_markdown(BROKEN_MD)
    check(len(rows) == 2, "broken sample: parsed %d rows, expected 2" % len(rows))
    issues = mod.compare(BROKEN_JSON, rows, folders=None, base=HERE)
    for expected in EXPECTED_BROKEN:
        check(expected in issues,
              "broken sample: missing expected finding %r; got %r" % (expected, issues))
    extra = [i for i in issues if i not in EXPECTED_BROKEN]
    check(extra == [], "broken sample: unexpected finding(s) %r" % extra)
    return "broken sample: 2 row(s), %d issue(s), all expected" % len(issues)


def test_folder(mod):
    with open(os.path.join(HERE, "index.json"), encoding="utf-8") as fh:
        index = json.load(fh)
    with open(os.path.join(HERE, "index.md"), encoding="utf-8") as fh:
        md = fh.read()
    check("v4" in md, "this folder's index.md carries no v4 marker")
    rows = mod.parse_markdown(md)
    check(len(rows) == len(index.get("entries", [])),
          "this folder: %d rows vs %d entries" % (len(rows), len(index.get("entries", []))))
    issues = mod.compare(index, rows, folders=None, base=HERE)
    check(issues == [], "this folder: expected 0 issues, got %r" % issues)
    names = [r["path"].strip("/") for r in rows]
    present = [n for n in names if os.path.isdir(os.path.join(HERE, n))]
    check(present != [], "no fixture folder in the index exists on disk")
    issues = mod.compare(index, rows, folders=present, base=HERE)
    check(issues == [], "this folder fixtures: expected 0 issues, got %r" % issues)
    return "this folder: %d row(s), 0 issue(s), %d fixture(s) present" % (len(rows), len(present))


def main():
    try:
        ic = import_tool("index_check")
        lines = [test_clean(ic), test_broken(ic), test_folder(ic)]
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
