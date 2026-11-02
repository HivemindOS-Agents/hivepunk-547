#!/usr/bin/env python3
# Self-test for csv-sample's reconcile_notes tool.
# Run with NO arguments, from this folder. No network. Writes only to a temp dir.
# It builds a small fixture, imports reconcile_notes, runs reconcile() on it and
# compares the plan with what should come out. Exits 0 only if every check passes.

import csv
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def die(msg):
    sys.stderr.write("FAIL: %s\n" % msg)
    sys.exit(1)


def build():
    d = tempfile.mkdtemp(prefix="csvsample-")
    hand = os.path.join(d, "hand.csv")
    comp = os.path.join(d, "computed.json")
    rows = [
        {"id": "L001", "expected_labels": "", "note": ""},
        {"id": "L004", "expected_labels": "empty_text", "note": ""},
        {"id": "L018", "expected_labels": "missing_source", "note": "a note"},
    ]
    with open(hand, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "expected_labels", "note"],
                           lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    computed = {"L001": ["empty_text"], "L004": ["empty_text", "fields"],
                "L018": ["missing_source"]}
    json.dump(computed, open(comp, "w", encoding="utf-8"))
    return d, hand, comp


def main():
    import reconcile_notes as rn
    d, hand, comp = build()
    res = rn.reconcile(hand, comp)

    add_ids = [p["id"] for p in res["add"]]
    drop_ids = [p["id"] for p in res["drop"]]

    if add_ids != ["L001", "L004"]:
        die("ADD ids are %r" % add_ids)
    if drop_ids != ["L018"]:
        die("DROP ids are %r" % drop_ids)
    if res["ok"] != 0:
        die("expected 0 OK rows, got %d" % res["ok"])
    if res["wrote"]:
        die("dry run should not write")

    # after --write the plan must be empty (idempotent)
    rn.reconcile(hand, comp, write=True)
    res2 = rn.reconcile(hand, comp)
    if len(res2["add"]) or len(res2["drop"]):
        die("after write the plan should be empty: add=%r drop=%r"
            % ([p["id"] for p in res2["add"]], [p["id"] for p in res2["drop"]]))
    if res2["ok"] != 3:
        die("after write all rows should be OK, got %d" % res2["ok"])

    # read the written file back and check the note column moved as planned
    with open(hand, encoding="utf-8", newline="") as fh:
        back = {r["id"]: r for r in csv.DictReader(fh)}
    if not back["L001"]["note"].strip() or not back["L004"]["note"].strip():
        die("written rows missing notes: %r" % back)
    if back["L018"]["note"].strip():
        die("L018 note was not dropped")

    print("PASS reconcile_notes: dry run planned ADD=%s DROP=%s"
          % (",".join(add_ids), ",".join(drop_ids)))
    print("PASS reconcile_notes: --write applied, re-run plan empty, OK=3")
    print("PASS column readback: notes present on L001/L004, dropped on L018")
    print("All self-tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
