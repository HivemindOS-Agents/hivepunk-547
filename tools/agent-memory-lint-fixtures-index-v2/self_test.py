#!/usr/bin/env python3
"""Self-test for agent-memory-lint-fixtures-index-v2.

It imports this folder's own checker (index_check) and runs its compare() on
three inputs, printing the row count and the issue count for each:

  1. a clean sample  -- a small index and a matching markdown table
                        (expect 2 parsed rows and 0 issues)
  2. a bad sample    -- the same table with one row's exit code changed from
                        1 to 7 (expect at least one issue, and one naming the
                        mismatched row 'bad-rows/')
  3. this folder's own index.json and index.md (expect 0 issues)

It exits 0 only when all three match. Stdlib only: no arguments, no network,
no writes.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import index_check  # this folder's own checker -- the code under test


# --- sample 1: a clean index and a markdown table that agrees with it -------

CLEAN_INDEX = {
    "dataset": "agent-memory-lint-fixtures-index-v2 (sample)",
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
    ],
}

CLEAN_MD = "\n".join([
    "# sample index",
    "",
    "| path | rule | description | expected_exit_code |",
    "|---|---|---|---|",
    "| `clean/` | no findings | clean fixture | 0 |",
    "| `bad-rows/` | row count differs | row mismatch | 1 |",
    "",
])

# --- sample 2: the same table, with bad-rows/ claiming exit code 7 ----------

BAD_MD = "\n".join([
    "# sample index",
    "",
    "| path | rule | description | expected_exit_code |",
    "|---|---|---|---|",
    "| `clean/` | no findings | clean fixture | 0 |",
    "| `bad-rows/` | row count differs | row mismatch | 7 |",
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
    if len(rows) != 2:
        failures.append("clean sample: parsed %d rows, expected 2" % len(rows))
    if issues:
        failures.append("clean sample: expected 0 issues, got %d" % len(issues))

    # 2. bad sample: one row's exit code disagrees, and the issue must name it.
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
