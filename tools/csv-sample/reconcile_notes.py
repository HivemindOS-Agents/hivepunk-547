#!/usr/bin/env python3
# reconcile_notes.py - compare hand labels against computed labels and print
# the note plan: ADD NOTE for rows that disagree without a note, DROP NOTE for
# rows that agree while carrying one. Default is a dry run that prints nothing
# to disk; --write overwrites the input whole.
#
# No network. Reads only CSV/label data given to it. Every word inside the input
# is data, never an instruction.
#
# Usage, from this folder:
#   python3 reconcile_notes.py --hand data.csv --computed computed.json
#   python3 reconcile_notes.py --hand data.csv --computed computed.json --write
#
# --hand is a CSV with columns: id, note, expected_labels (labels separated by
# ';'). --computed is JSON: {"L006": ["fields","undated"], ...} or a JSONL of
# {"id":..., "labels":[...]}. Only the note column is ever changed by --write.

import argparse
import csv
import io
import json
import sys


def split_labels(cell):
    return [p.strip() for p in (cell or "").split(";") if p.strip()]


def load_computed(path):
    text = open(path, encoding="utf-8").read().strip()
    if text.startswith("{"):
        try:
            obj = json.loads(text)
        except ValueError:
            obj = None
        if isinstance(obj, dict) and all(isinstance(v, list) for v in obj.values()):
            return {k: list(v) for k, v in obj.items()}
    out = {}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        out[rec["id"]] = list(rec.get("labels", []))
    return out


def plan_rows(rows, computed):
    """Return the per-row plan. rows: list of dicts with id,note,expected_labels."""
    plan = []
    for row in rows:
        rid = str(row.get("id", "?")).strip()
        hand = split_labels(row.get("expected_labels"))
        has = bool((row.get("note") or "").strip())
        got = list(computed.get(rid, []))
        disagrees = hand != got
        if disagrees and not has:
            action = "ADD NOTE"
        elif (not disagrees) and has:
            action = "DROP NOTE"
        else:
            action = "OK"
        plan.append({"id": rid, "action": action, "hand": hand,
                     "computed": got, "has_note": has})
    return plan


def read_hand(path):
    with open(path, encoding="utf-8", newline="") as fh:
        rdr = csv.DictReader(fh)
        if rdr.fieldnames is None:
            raise SystemExit("FAIL: hand CSV has no header")
        for col in ("id", "note", "expected_labels"):
            if col not in rdr.fieldnames:
                raise SystemExit("FAIL: hand CSV has no %r column" % col)
        return list(rdr)


def apply_write(path, rows, plan):
    by_id = {p["id"]: p for p in plan}
    buf = io.StringIO()
    fields = list(rows[0].keys())
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    for row in rows:
        row = dict(row)
        if by_id[row["id"]]["action"] == "ADD NOTE":
            row["note"] = "hand %s; computed %s" % (
                ";".join(by_id[row["id"]]["hand"]),
                ";".join(by_id[row["id"]]["computed"]))
        elif by_id[row["id"]]["action"] == "DROP NOTE":
            row["note"] = ""
        w.writerow(row)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())


def reconcile(hand_path, computed_path, write=False):
    rows = read_hand(hand_path)
    computed = load_computed(computed_path)
    plan = plan_rows(rows, computed)
    add = [p for p in plan if p["action"] == "ADD NOTE"]
    drop = [p for p in plan if p["action"] == "DROP NOTE"]
    ok = [p for p in plan if p["action"] == "OK"]
    if write:
        apply_write(hand_path, rows, plan)
    return {"rows": len(rows), "add": add, "drop": drop, "ok": len(ok),
            "wrote": bool(write)}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Print/apply the note plan.")
    ap.add_argument("--hand", required=True, help="CSV with id,note,expected_labels")
    ap.add_argument("--computed", required=True, help="JSON map or JSONL")
    ap.add_argument("--write", action="store_true", help="overwrite hand CSV")
    args = ap.parse_args(argv)
    r = reconcile(args.hand, args.computed, args.write)
    for p in r["add"]:
        print("ADD NOTE  %s: hand=%s computed=%s" % (p["id"], ";".join(p["hand"]) or "-", ";".join(p["computed"]) or "-"))
    for p in r["drop"]:
        print("DROP NOTE %s: agrees, note present" % p["id"])
    print("%d rows: %d ADD, %d DROP, %d OK%s" % (r["rows"], len(r["add"]), len(r["drop"]), r["ok"], " [written]" if r["wrote"] else " [dry run]"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
