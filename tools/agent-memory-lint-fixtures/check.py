#!/usr/bin/env python3
"""Unmodified checker for the agent‑memory‑lint fixtures dataset.

The script expects a JSONL file of records and outputs a JSON mapping from
record ``id`` to the list of lint rule names that the record violates.

The implementation mirrors the original project: a light‑weight structural
check based solely on the presence and format of the fields.

Usage:
    python3 check.py records.jsonl > got.json

The output can be compared to ``expected_labels.json``.  No network access or
side effects occur.
"""

import json, sys
from datetime import date

ALLOWED_FIELDS = {"id", "text", "source", "as_of", "tags"}
CUTOFF_DATE = date(2026, 10, 27)


def lint(record):
    issues = set()
    if set(record) != ALLOWED_FIELDS:
        issues.add("fields")
    if not isinstance(record.get("text"), str) or not record.get("text", "").strip():
        issues.add("empty_text")
    if not record.get("source"):
        issues.add("missing_source")
    raw_as_of = record.get("as_of")
    if not raw_as_of:
        issues.add("undated")
    else:
        try:
            if date.fromisoformat(raw_as_of) < CUTOFF_DATE:
                issues.add("stale")
        except ValueError:
            issues.add("undated")
    return sorted(issues)


def main(path):
    results = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            results[rec["id"]] = lint(rec)
    print(json.dumps(results, sort_keys=True, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 check.py <records.jsonl>")
    main(sys.argv[1])
