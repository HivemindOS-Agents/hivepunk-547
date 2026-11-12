#!/usr/bin/env python3
"""Self-test for agent-memory-lint-fixtures-index-v3.

See ../agent-memory-lint-fixtures-index-v2/self_test.py for the v2 version.
This version modifies the bad-sample case: instead of differing exit codes, it
changes the path so the markdown row no longer matches an index entry.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import index_check


# --- sample 1: a clean index and a markdown table that agrees with it -------
# Must include all three known fixture directories so the missing-known-fixture
# check does not fire.  This matches the folder's own index.json which has
# entries for clean/, bad-rows/ and bad-card/.

CLEAN_INDEX = {
    "dataset": "agent-memory-lint-fixtures-index-v3 (sample)",
    "fixtures_root": "fixtures/",
    "version": 2,
    "entries": [
        {
            "path": "clean/",
            "rule": "no findings",
            "description": "clean fixture",
            "expected_exit_code": 0,
        },
        {
            "path": "bad-rows/",
            "rule": "row count differs",
            "description": "row mismatch",
            "expected_exit_code": 1,
        },
        {
            "path": "bad-card/",
            "rule": "missing closing section",
            "description": "card missing closing what-could-not-be-checked",
            "expected_exit_code": 1,
        },
    ],
}

CLEAN_MD = "\n".join([
    "# sample index",
    "",
    "| path | rule | description | expected_exit_code |",
    "|---|---|---|---|",
    "| `clean/` | no findings | clean fixture | 0 |",
    "| `bad-rows/` | row count differs | row mismatch | 1 |",
    "| `bad-card/` | missing closing section | card missing closing what-could-not-be-checked | 1 |",
    "",
])

# --- sample 2: the same table, but bad-rows/ renamed in the markdown to
#               fixtures/bad-rows/ (mismatch with index entry 'bad-rows/')

BAD_MD = "\n".join([
    "# sample index",
    "",
    "| path | rule | description | expected_exit_code |",
    "|---|---|---|---|",
    "| `clean/` | no findings | clean fixture | 0 |",
    "| `fixtures/bad-rows/` | row count differs | row mismatch | 1 |",
    "",
])


def report(label, rows, issues):
    print("%s: %d row(s), %d issue(s)" % (label, len(rows), len(issues)))
    for issue in issues:
        print("    - " + issue)


def read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def main():
    failures = []

    # 1. clean sample: the checker must find nothing wrong.
    rows = index_check.parse_index_md(CLEAN_MD)
    issues = index_check.compare(CLEAN_INDEX, rows)
    report("clean sample", rows, issues)
    if len(rows) != 3:
        failures.append("clean sample: parsed %d rows, expected 3" % len(rows))
    if issues:
        failures.append("clean sample: expected 0 issues, got %d" % len(issues))

    # 2. bad sample: one row's path disagrees; the issue must name it.
    rows = index_check.parse_index_md(BAD_MD)
    issues = index_check.compare(CLEAN_INDEX, rows)
    report("bad sample", rows, issues)
    if not issues:
        failures.append("bad sample: expected at least 1 issue, got 0")
    elif not any("bad-rows/" in issue for issue in issues):
        failures.append("bad sample: no issue names the mismatched row bad-rows/")

    # 3. this folder's own index.json and index.md must agree.
    own_rows = index_check.parse_index_md(read_text(os.path.join(HERE, "index.md")))
    own_index = index_check.load_index(os.path.join(HERE, "index.json"))
    issues = index_check.compare(own_index, own_rows)
    report("this folder", own_rows, issues)
    if not own_rows:
        failures.append("this folder: parsed 0 rows from index.md")
    if issues:
        failures.append("this folder: expected 0 issues, got %d" % len(issues))

    if failures:
        for line in failures:
            sys.stderr.write("FAIL: " + line + "\n")
        return 1

    print("self-test: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
