#!/usr/bin/env python3
"""Self‑test for the agent‑memory‑lint‑fixtures package.

It validates that
  * ``records.jsonl`` is a sequence of valid JSON objects;
  * ``expected_labels.json`` is a JSON mapping with the same set of record IDs;
  * the keys in ``expected_labels.json`` are in canonical sorted order.

The script exits with code 0 if all checks pass, otherwise it prints a
human‑readable error message and exits with code 1.
"""

import json, sys, os

RECORDS_FILE = "records.jsonl"
LABELS_FILE = "expected_labels.json"


def load_records(path):
    records = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Malformed JSON in {path}: {e}")
                sys.exit(1)
    return records


def load_labels(path):
    with open(path, encoding="utf-8") as fh:
        try:
            return json.load(fh)
        except json.JSONDecodeError as e:
            print(f"Malformed JSON in {path}: {e}")
            sys.exit(1)


def main():
    if not os.path.isfile(RECORDS_FILE) or not os.path.isfile(LABELS_FILE):
        print("Required input files not found.")
        sys.exit(1)

    recs = load_records(RECORDS_FILE)
    labels = load_labels(LABELS_FILE)

    rec_ids = {r.get("id") for r in recs}
    label_ids = set(labels.keys())

    missing = rec_ids - label_ids
    extra = label_ids - rec_ids

    if missing or extra:
        if missing:
            print(f"IDs present in records.jsonl but missing from expected_labels.json: {sorted(missing)}")
        if extra:
            print(f"IDs present in expected_labels.json but missing from records.jsonl: {sorted(extra)}")
        sys.exit(1)

    # Check that keys are sorted alphabetically
    if list(labels.keys()) != sorted(labels.keys()):
        print("expected_labels.json keys are not sorted alphabetically.")
        sys.exit(1)

    print("Self‑test passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
