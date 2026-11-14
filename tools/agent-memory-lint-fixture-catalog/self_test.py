#!/usr/bin/env python3
"""Self-test for agent-memory-lint-fixture-catalog.

Run with no arguments, from this folder. No network, no writes. Exits 0 only
when every check passes.

It imports generate_catalog.py, runs its embedded pipeline, compares the
resulting CSV with the shipped catalog.csv, and verifies the CSV content is
correct.
"""

import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def import_tool(name):
    sys.dont_write_bytecode = True
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    return __import__(name)


def check(cond, msg):
    if not cond:
        sys.stderr.write("FAIL: %s\n" % msg)
        sys.exit(1)


def main():
    try:
        gc = import_tool("generate_catalog")
    except Exception as e:
        sys.stderr.write("FAIL: could not import generate_catalog: %s\n" % e)
        return 1

    # 1. Generate CSV from embedded sample
    csv_text = gc.process(embedded=True)
    reader = csv.reader(io.StringIO(csv_text))
    rows = list(reader)
    check(len(rows) == 4, "expected 4 rows (1 header + 3 data), got %d" % len(rows))

    # 2. Check header
    header = rows[0]
    expected_header = ["fixture", "rule", "expected_exit_code", "what_it_trips"]
    check(header == expected_header, "header mismatch: %r" % header)

    # 3. Check data rows
    data = rows[1:]
    expected_data = [
        ["fixtures/clean/", "no findings on a clean fixture", "0", "nothing - lint walks it and exits clean"],
        ["fixtures/bad-rows/", "row count or empty-cell finding", "1", "a data row whose cell count does not match the header"],
        ["fixtures/bad-card/", "missing closing 'What could not be checked' section", "1", "a card that ends without its closing section"],
    ]
    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        check(actual == expected,
              "data row %d: expected %r, got %r" % (i+2, expected, actual))

    # 4. Compare with shipped catalog.csv
    shipped_path = os.path.join(HERE, "catalog.csv")
    check(os.path.isfile(shipped_path), "catalog.csv not found at %s" % shipped_path)
    with open(shipped_path, "r", encoding="utf-8") as fh:
        shipped_text = fh.read()
    check(csv_text == shipped_text,
          "generated CSV does not match shipped catalog.csv")

    # 5. Test the check method
    check_ok = gc.check(csv_path=shipped_path, embedded=True)
    check(check_ok, "generate_catalog --check failed")

    print("generated CSV matches expected values and shipped catalog.csv")
    print("self-test: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
