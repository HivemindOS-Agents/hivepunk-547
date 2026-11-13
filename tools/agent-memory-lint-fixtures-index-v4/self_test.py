#!/usr/bin/env python3
"""Top-of-folder self-test for agent-memory-lint-fixtures-index-v4.

Run with no arguments, from this folder. No network, no writes. Exits 0 only
when every check passes.

It imports the tool's own code (index_check.parse_markdown, index_check.compare,
readback.listing_rows, readback.listing_verdict, readback.compare_bytes) and runs
it on bundled sample data:

  * a clean sample of three entries and three matching rows -> 0 issues
  * a deliberately broken sample: three JSON entries, a two-row table, and
    three mutated values -> exactly four issues, asserted one by one
  * this folder's own index.json + index.md pair -> 0 issues
  * the folder check over the three declared fixtures -> 0 issues
  * readback: every file decided by the sha256 of its bytes; a rewrapped
    index.md with the same byte length and a different sha256 is caught and
    the verdict is FAIL; a same-bytes file with a different 40-hex git blob id
    is caught through the second fingerprint; a 64-hex id is not a git blob id
  * readback: an extra LICENSE row raises the licence-rule issue and the
    unexpected-row finding. The shipped listing_verdict() accepts a 5- or
    6-row window, so the six-row LICENSE sample is inside it and raises NO
    row-count finding; this test asserts only the two findings that are
    actually produced.

A table with no issues is not called correct here; each expected finding is
named and compared.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

CLEAN_JSON = {
    "entries": [
        {"path": "clean/", "rule": "no findings on a clean fixture", "expected_exit_code": 0},
        {"path": "bad-rows/", "rule": "row count or empty-cell finding", "expected_exit_code": 1},
        {"path": "bad-card/", "rule": "missing closing 'What could not be checked' section", "expected_exit_code": 1},
    ]
}

CLEAN_MD = (
    "# sample\n\n"
    "| Path | Rule | Expected exit code |\n"
    "|---|---|---|\n"
    "| `clean/` | no findings on a clean fixture | 0 |\n"
    "| `bad-rows/` | row count or empty-cell finding | 1 |\n"
    "| `bad-card/` | missing closing 'What could not be checked' section | 1 |\n"
)

BROKEN_JSON = {
    "entries": [
        {"path": "clean/", "rule": "no findings on a clean fixture", "expected_exit_code": 0},
        {"path": "bad-rows/", "rule": "row count or empty-cell finding", "expected_exit_code": 1},
        {"path": "bad-card/", "rule": "missing closing 'What could not be checked' section", "expected_exit_code": 1},
    ]
}

# Two rows: bad-card row missing, clean row's rule mutated, bad-rows code flipped.
BROKEN_MD = (
    "| Path | Rule | Expected exit code |\n"
    "|---|---|---|\n"
    "| `clean/` | findings are expected everywhere | 0 |\n"
    "| `bad-rows/` | row count or empty-cell finding | 0 |\n"
)

EXPECTED_BROKEN = [
    "count mismatch: index has 3 entries, markdown has 2 rows",
    "entry 'bad-card/' in index but not in markdown",
    "row 'clean/': rule differs: markdown='findings are expected everywhere' index='no findings on a clean fixture'",
    "row 'bad-rows/': expected_exit_code differs: index=1 markdown=0",
]

FIXTURES = ["clean", "bad-rows", "bad-card"]


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
    mod = __import__(name)
    return mod


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
    issues = mod.compare(index, rows, folders=names, base=HERE)
    check(issues == [], "this folder fixtures: expected 0 issues, got %r" % issues)
    return "this folder: %d row(s), 0 issue(s), fixtures present" % len(rows)


def test_readback(mod):
    # A clean listing passes the shape check and every row carries a 40-hex id.
    rows = mod.listing_rows(mod.SAMPLE_TREE)
    check(len(rows) == 5, "readback: sample listing has %d rows, expected 5" % len(rows))
    issues = mod.listing_verdict(rows)
    check(issues == [], "readback: clean sample listing raised %r" % issues)
    for r in rows:
        check(mod.is_git_oid(r["hub_oid"]),
              "readback: no 40-hex object id read for %r" % r["path"])

    # The rewrapped fixture must have the same byte length as the clean one
    # and a different sha256: that is what makes it a genuine rewrap.
    clean = mod.INDEX_MD_CLEAN
    rewrapped = mod.INDEX_MD_REWRAPPED
    check(len(clean) == len(rewrapped),
          "readback: rewrap changed byte length, %d vs %d" % (len(clean), len(rewrapped)))
    check(mod.sha256(clean) != mod.sha256(rewrapped),
          "readback: rewrap did not change sha256; the broken sample is byte-identical")

    # Byte-identical sample passes; the verdict must be PASS.
    byte_rows, byte_issues = mod.sample_compare(diff=False)
    check(byte_issues == [], "readback: clean sample bytes raised %r" % byte_issues)
    for r in byte_rows:
        check(r["length_equal"], "readback: clean sample %r length differs" % r["path"])
        check(r["sha256_equal"], "readback: clean sample %r sha256 differs" % r["path"])
        check(r["oid_equal"] is True,
              "readback: clean sample %r oid_equal=%r" % (r["path"], r["oid_equal"]))
        check(r["content_equal"], "readback: clean sample %r not decided equal" % r["path"])
    line = mod.verdict_line(byte_rows, [], [])
    check(line == "verdict: PASS", "readback: clean sample verdict %r" % line)

    # A rewrapped index.md must be caught by the sha256 comparison, at the
    # same byte length, and the verdict must be FAIL.
    bad_rows, bad_issues = mod.sample_compare(diff=True)
    check(any("index.md" in i and "sha256 differs" in i for i in bad_issues),
          "readback: rewrapped index.md not caught; issues=%r" % bad_issues)
    check(not any("index.md" in i and "length differs" in i for i in bad_issues),
          "readback: rewrap reported as a length difference; issues=%r" % bad_issues)
    rw = [r for r in bad_rows if r["path"] == "index.md"]
    check(len(rw) == 1, "readback: no index.md row in the rewrapped run")
    rw = rw[0]
    check(rw["length_equal"], "readback: rewrapped index.md length_equal is False")
    check(not rw["sha256_equal"], "readback: rewrapped index.md sha256_equal is True")
    check(not rw["content_equal"], "readback: rewrapped index.md decided equal")
    line = mod.verdict_line(bad_rows, [], bad_issues)
    check(line == "verdict: FAIL", "readback: rewrapped verdict %r" % line)

    # Same bytes, different 40-hex git blob id: caught by the second check.
    same_rows, same_issues = mod.sample_compare(diff=False, gh_diff=True)
    check(any("index.md" in i and "git blob id differs" in i for i in same_issues),
          "readback: blob-id-only change not caught; issues=%r" % same_issues)
    rw = [r for r in same_rows if r["path"] == "index.md"][0]
    check(rw["sha256_equal"], "readback: blob-id run changed sha256_equal")
    check(rw["oid_equal"] is False, "readback: blob-id run oid_equal=%r" % rw["oid_equal"])
    check(not rw["content_equal"], "readback: blob-id run decided equal")
    line = mod.verdict_line(same_rows, [], same_issues)
    check(line == "verdict: FAIL", "readback: blob-id verdict %r" % line)

    # Only a full 40-hex id is a git blob id.
    check(mod.is_git_oid("a" * 40) is True, "readback: is_git_oid rejected 40 hex")
    check(mod.is_git_oid("a" * 64) is False, "readback: is_git_oid accepted 64 hex")
    check(mod.is_git_oid("") is False, "readback: is_git_oid accepted empty")
    check(mod.is_git_oid(None) is False, "readback: is_git_oid accepted None")
    check(mod.is_git_oid("g" * 40) is False, "readback: is_git_oid accepted non-hex")

    # An extra LICENSE row must fail on the rule and on the unexpected row.
    # The shipped listing_verdict() accepts a 5- or 6-row window, so the
    # six-row sample does NOT raise a row-count issue; assert only the two
    # findings the shipped code actually produces.
    rows = mod.listing_rows(mod.SAMPLE_TREE_EXTRA)
    check(len(rows) == 6, "readback: extra listing has %d rows, expected 6" % len(rows))
    issues = mod.listing_verdict(rows)
    check(any("LICENSE" in i for i in issues),
          "readback: LICENSE row not flagged; issues=%r" % issues)
    check(any("unexpected row" in i and "LICENSE" in i for i in issues),
          "readback: LICENSE row not flagged as unexpected; issues=%r" % issues)
    return ("readback: 5 rows, sha256 decides, rewrap caught, blob id caught,"
            " LICENSE flagged, row count not flagged (window)")


def main():
    try:
        check_mod = import_tool("index_check")
        lines = [test_clean(check_mod), test_broken(check_mod), test_folder(check_mod)]
        rb = import_tool("readback")
        lines.append(test_readback(rb))
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
