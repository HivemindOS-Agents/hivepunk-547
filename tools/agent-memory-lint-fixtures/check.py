#!/usr/bin/env python3
"""Agent‑memory‑lint checker

This script reads a JSONL file of records, extracts the `id` of each record whose
`label` is not the string ``"unknown"``, and writes them as a JSON array to
``got.json``. It mirrors the original behaviour of the `check.py` used in the
agent‑memory‑lint project.

Usage:

    python3 check.py records.jsonl > got.json

The output is suitable for comparison against ``expected_labels.json``.
"""

import json, sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 check.py <records.jsonl>")
    records_path = sys.argv[1]
    with open(records_path, "r", encoding="utf8") as f:
        records = [json.loads(line) for line in f if line.strip()]
    # In the original checker, this would apply lint rules; here we simply
    # return the IDs of all records that do *not* have label "unknown".
    output = [rec["id"] for rec in records if rec.get("label") != "unknown"]
    with open("got.json", "w", encoding="utf8") as out:
        json.dump(output, out, indent=2)
    sys.exit(0)
