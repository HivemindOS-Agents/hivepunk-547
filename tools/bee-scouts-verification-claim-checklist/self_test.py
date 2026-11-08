#!/usr/bin/env python3
# bee-scouts-verification-claim-checklist / self_test.py
# Run with NO arguments, no network, from this folder:
#     python3 self_test.py
# Reads data.csv and validates header, row count, cell count, verdict and source order.
# Exits 0 only when every check passes.

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "data.csv")

EXPECTED_HEADER = [
    "claim",
    "where_it_appears",
    "what_would_prove_it",
    "what_is_missing",
    "verdict",
    "source",
]

EXPECTED_VERDICTS = [
    "shown",
    "unshown",
    "unshown",
    "none-observed",
    "shown",
    "shown",
]

EXPECTED_SOURCES = [
    "https://github.com/HivemindOS-Agents/bee-scouts/issues/122",
    "https://github.com/LiamVisionary/bee-scouts/issues/32",
    "https://github.com/HivemindOS-Agents/bee-scouts/issues/85",
    "https://github.com/LiamVisionary/bee-scouts/issues/53",
    "https://github.com/HivemindOS-Agents/bee-scouts/issues/120",
    "https://github.com/LiamVisionary/bee-scouts/issues/43",
]

VERDICT_SET = {"shown", "unshown", "none-observed"}

class Checker:
    def __init__(self):
        self.failed = 0

    def check(self, ok, label, detail=""):
        if ok:
            sys.stdout.write(f"PASS {label}\n")
        else:
            self.failed += 1
            sys.stderr.write(f"FAIL {label}{(' -- ' + detail) if detail else ''}\n")


def main():
    c = Checker()

    if not os.path.isfile(CSV_PATH):
        c.check(False, "data.csv exists")
        sys.exit(1)

    with open(CSV_PATH, "r", encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        rows = list(reader)

    if not rows:
        c.check(False, "data.csv is not empty")
        sys.exit(1)

    header, *data_rows = rows
    c.check(header == EXPECTED_HEADER, "header is exactly the six expected columns", repr(header))

    c.check(len(data_rows) == 6, "exactly 6 data rows", str(len(data_rows)))

    for idx, row in enumerate(data_rows, start=1):
        c.check(len(row) == 6, f"row {idx} has six cells", f"got {len(row)} cells")
        if len(row) == 6:
            verdict, source = row[4], row[5]
            c.check(verdict in VERDICT_SET, f"row {idx} verdict is valid", verdict)
            c.check(source in EXPECTED_SOURCES, f"row {idx} source matches expected", source)
            if idx <= len(EXPECTED_VERDICTS):
                c.check(verdict == EXPECTED_VERDICTS[idx-1], f"row {idx} verdict matches order", verdict)
            if idx <= len(EXPECTED_SOURCES):
                c.check(source == EXPECTED_SOURCES[idx-1], f"row {idx} source matches order", source)

    if c.failed:
        sys.stderr.write(f"self-test FAILED: {c.failed} check(s) failed\n")
        sys.exit(1)
    sys.stdout.write("OK self-test passed: 6 claim rows, header and order verified.\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
