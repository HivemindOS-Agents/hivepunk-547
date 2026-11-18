#!/usr/bin/env python3
"""Self-test for the fixtures-index-v4 dataset package.

Run from this folder with no arguments and no network. Validates
data/data.csv: header, non-empty fields, unique tool_names,
well-formed http/https source URLs, and the expected 3-row set.
Exits 0 only if every check passes.
"""

import csv
import os
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "data.csv")
EXPECTED_HEADER = ["tool_name", "description", "detail", "source"]
EXPECTED_TOOLS = {"dataset-manifest-check", "csv-schema-check", "artifacts-index-check"}
INVALID = set(' <>"\'{}|^`')


class Fail(Exception):
    pass


def check(cond, msg):
    if not cond:
        raise Fail(msg)


def is_url(value):
    if not value or any(c in INVALID for c in value):
        return False
    try:
        parts = urllib.parse.urlparse(value)
    except ValueError:
        return False
    if parts.scheme not in ("http", "https") or not parts.netloc:
        return False
    host = parts.hostname
    return bool(host) and (host == "localhost" or "." in host)


def main():
    checks = []
    try:
        check(os.path.isfile(DATA), "data/data.csv not found at %s" % DATA)
        check(os.path.isfile(os.path.join(HERE, "README.md")), "README.md not found")
        with open(DATA, encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            header = reader.fieldnames or []
            rows = list(reader)
        check(header == EXPECTED_HEADER, "header %r != %r" % (header, EXPECTED_HEADER))
        checks.append("header is tool_name,description,detail,source")
        check(len(rows) == 3, "expected 3 data rows, got %d" % len(rows))
        checks.append("exactly 3 data rows")
        names = []
        for i, row in enumerate(rows, 1):
            for col in EXPECTED_HEADER:
                check((row.get(col) or "").strip(), "row %d: field %s is empty" % (i, col))
            check(is_url(row["source"].strip()), "row %d: source is not a well-formed http/https URL: %r" % (i, row["source"]))
            names.append(row["tool_name"].strip())
        check(len(set(names)) == len(names), "tool_name values are not unique: %r" % (names,))
        check(set(names) == EXPECTED_TOOLS, "tool_name set %r != %r" % (set(names), EXPECTED_TOOLS))
        checks.append("all fields populated, sources well-formed, tool_names unique and as expected")
        for name, row in zip(names, rows):
            check("hivepunk-547" in row["source"], "%s: source does not reference hivepunk-547" % name)
            check("/tools/" + name in row["source"], "%s: source does not point at its tools folder" % name)
        checks.append("each source points at its tools/<tool_name> folder")
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
