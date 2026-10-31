#!/usr/bin/env python3
# UNTESTED - hand-derived helper. Written, not executed by this step.
# No network, no writes outside the path you pass. No process is run for you.
#
# Turns records.jsonl + expected_labels.json into one row per record, with a
# HAND-DERIVED checker label list, an agreement flag and a mismatch note.
#
# Usage:
#   python3 build_labelled_rows.py records.jsonl expected_labels.json > labelled_rows.csv
#
# The checker logic below mirrors check.py's rules, read by hand from its code.
# It is NOT a captured checker run: there is no exit code, stdout or diff here.
# Self-agreement between these columns is not accuracy against any real store.

import csv
import json
import sys
from datetime import date

ALLOWED = {"id", "text", "source", "as_of", "tags"}
CUTOFF = date(2026, 10, 27)
MISMATCH_NOTE = {
    "fields": "fields rule fires when the key set differs from the 5 allowed keys",
    "undated": "no as_of key",
    "missing_source": "no source key",
}


def checker_labels(rec):
    """Hand-derived from check.py's rules. Not a captured run."""
    out = set()
    if set(rec) != ALLOWED:
        out.add("fields")
    text = rec.get("text")
    if not isinstance(text, str) or not text.strip():
        out.add("empty_text")
    if not rec.get("source"):
        out.add("missing_source")
    raw = rec.get("as_of")
    if not raw:
        out.add("undated")
    else:
        try:
            if date.fromisoformat(raw) < CUTOFF:
                out.add("stale")
        except ValueError:
            out.add("undated")
    return sorted(out)


def note_for(exp, got):
    if exp == got:
        return ""
    only = sorted(set(got) - set(exp))
    if only == ["fields"]:
        return ("fields fires alongside the key-specific rule the hand label "
                "recorded (missing/extra key); labelling dispute, not a bug")
    parts = [MISMATCH_NOTE.get(r, r) for r in only]
    return "; ".join(parts) or "label sets differ"


def main():
    if len(sys.argv) != 3:
        sys.stderr.write(
            "Usage: python3 build_labelled_rows.py records.jsonl expected_labels.json\n")
        return 2
    records = []
    with open(sys.argv[1], encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                records.append(json.loads(line))
    with open(sys.argv[2], encoding="utf-8") as fh:
        expected = json.load(fh)

    w = csv.writer(sys.stdout)
    w.writerow(["id", "text", "source", "as_of", "tags",
                "expected_labels", "checker_labels", "agree", "note"])
    agree_n = 0
    for rec in records:
        rid = rec.get("id", "")
        exp = list(expected.get(rid, []))
        got = checker_labels(rec)
        ok = "true" if exp == got else "false"
        if exp == got:
            agree_n += 1
        w.writerow([
            rid,
            rec.get("text", ""),
            rec.get("source", ""),
            rec.get("as_of", ""),
            " ".join(rec.get("tags", [])),
            " ".join(exp),
            " ".join(got),
            ok,
            note_for(exp, got),
        ])
    sys.stderr.write(
        "hand-derived: %d/%d agree; self-agreement is not accuracy; "
        "no run, no exit code, no diff\n" % (agree_n, len(records)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
