#!/usr/bin/env python3
# Self-test for the agent-memory-lint-fixtures tool folder.
# Run with NO arguments, from this folder. No network, no writes.
# Exits 0 only when every check passes.

import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def die(msg):
    sys.stderr.write("FAIL: %s\n" % msg)
    sys.exit(1)


def load_records(path):
    recs = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                try:
                    recs.append(json.loads(line))
                except json.JSONDecodeError as e:
                    die("malformed JSON in %s: %s" % (path, e))
    return recs


def main():
    rec_path = os.path.join(HERE, "records.jsonl")
    lab_path = os.path.join(HERE, "expected_labels.json")
    for p in (rec_path, lab_path):
        if not os.path.isfile(p):
            die("missing required file: %s" % p)

    recs = load_records(rec_path)
    if len(recs) != 20:
        die("expected 20 records, found %d" % len(recs))
    ids = [r["id"] for r in recs]
    if len(set(ids)) != 20:
        die("record ids are not unique")

    with open(lab_path, encoding="utf-8") as fh:
        expected = json.load(fh)
    if set(expected.keys()) != set(ids):
        die("expected_labels.json ids do not match records.jsonl ids")
    if list(expected.keys()) != sorted(expected.keys()):
        die("expected_labels.json keys are not in canonical sorted order")
    for k, v in expected.items():
        if not isinstance(v, list):
            die("label for %s is not a list" % k)

    # import the builder without running its main()
    sys.path.insert(0, HERE)
    try:
        import build_labelled_rows as b
    except Exception as e:
        die("cannot import build_labelled_rows: %s" % e)

    agree = 0
    mismatches = []
    for rec in recs:
        exp = list(expected[rec["id"]])
        got = b.checker_labels(rec)
        if exp == got:
            agree += 1
            if b.note_for(exp, got) != "":
                die("row %s agrees but has a note" % rec["id"])
        else:
            mismatches.append(rec["id"])
            if b.note_for(exp, got) == "":
                die("row %s disagrees but has no note" % rec["id"])

    if agree != 17:
        die("hand-derived agreement is %d/20, expected 17/20" % agree)
    if mismatches != ["L006", "L015", "L018"]:
        die("mismatching ids are %r, expected ['L006','L015','L018']" % mismatches)

    print("Self-test passed: 20 records, hand-derived agreement 17/20, "
          "mismatches L006/L015/L018, every row noted. "
          "No checker was run; no exit code, stdout or diff exists.")
    sys.exit(0)


if __name__ == "__main__":
    main()
