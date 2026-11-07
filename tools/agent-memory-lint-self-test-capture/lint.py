#!/usr/bin/env python3
"""Lint checker for memory JSONL records.

Reads a JSONL file, checks each record for missing ``as_of`` and
missing ``source``, and prints one line per finding in the format:

    <id>: missing <field>

Exit code is 0 if all records are valid, 1 otherwise.

No network. Reads only the given file.
"""

import json
import sys
from pathlib import Path


def lint(records):
    """Yield (id, field) tuples for each missing field found."""
    for rec in records:
        rid = rec.get("id", "?")
        if not rec.get("as_of", "").strip():
            yield rid, "as_of"
        if not rec.get("source", "").strip():
            yield rid, "source"


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        sys.stderr.write("usage: python3 lint.py <jsonl_file>\n")
        return 1
    path = Path(argv[0])
    if not path.is_file():
        sys.stderr.write(f"error: file not found: {path}\n")
        return 1

    with open(path, "r", encoding="utf-8") as fh:
        records = [json.loads(line) for line in fh if line.strip()]

    findings = list(lint(records))
    for rid, field in findings:
        print(f"{rid}: missing {field}")

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
