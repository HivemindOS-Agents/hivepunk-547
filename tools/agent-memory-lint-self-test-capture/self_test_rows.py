#!/usr/bin/env python3
# Row-integrity self-test for the captured fixtures.
# Run with NO arguments, from this folder. No network, no writes.
# Exits 0 only when every check passes.

import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COLS = ["id", "text", "source", "as_of", "tags",
        "expected_labels", "checker_labels", "agree", "note"]
EXPECTED_IDS = ["L%03d" % n for n in range(1, 21)]
MISMATCHES = ["L006", "L015", "L018"]


def die(msg):
    sys.stderr.write("FAIL: %s\n" % msg)
    sys.exit(1)


def split_labels(cell):
    return [p for p in cell.split(";") if p]


def main():
    path = os.path.join(HERE, "data.csv")
    if not os.path.isfile(path):
        die("missing data.csv")
    with open(path, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    if list(rows[0].keys()) != COLS:
        die("header is %r, expected %r" % (list(rows[0].keys()), COLS))
    if len(rows) != 20:
        die("expected 20 rows, found %d" % len(rows))

    ids = [r["id"] for r in rows]
    if ids != EXPECTED_IDS:
        die("ids are %r, expected L001-L020 in order" % ids)

    agree = 0
    mismatches = []
    for r in rows:
        exp = split_labels(r["expected_labels"])
        got = split_labels(r["checker_labels"])
        flag = r["agree"]
        note = r["note"].strip()
        if flag not in ("true", "false"):
            die("row %s has agree=%r" % (r["id"], flag))
        same = exp == got
        if same != (flag == "true"):
            die("row %s agree=%s but label lists %s" % (r["id"], flag,
                "match" if same else "differ"))
        if same:
            agree += 1
            if note:
                die("row %s agrees but carries a note" % r["id"])
        else:
            mismatches.append(r["id"])
            if not note:
                die("row %s disagrees but has no note" % r["id"])

    if agree != 17:
        die("agreement is %d/20, expected 17/20" % agree)
    if mismatches != MISMATCHES:
        die("mismatches are %r, expected L006/L015/L018" % mismatches)

    # The capture fixtures must exist and must not pretend to be a run.
    for name in ("run.stdout.txt", "run.meta.txt"):
        p = os.path.join(HERE, "fixtures", name)
        if not os.path.isfile(p):
            die("missing fixtures/%s" % name)
    meta = open(os.path.join(HERE, "fixtures", "run.meta.txt"),
                encoding="utf-8").read()
    if "exit_code:" not in meta:
        die("fixtures/run.meta.txt has no exit_code line")
    out = open(os.path.join(HERE, "fixtures", "run.stdout.txt"),
               encoding="utf-8").read()
    if not out.strip():
        die("fixtures/run.stdout.txt is empty")

    print("Self-test passed: 20 rows, ids L001-L020, agreement 17/20, "
          "mismatches L006/L015/L018, only disagreeing rows have notes, "
          "capture fixtures present. No checker was run by this step.")
    sys.exit(0)


if __name__ == "__main__":
    main()
