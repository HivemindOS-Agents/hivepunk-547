#!/usr/bin/env python3
"""Generate or check catalog.csv for agent-memory-lint-fixture-catalog.

Usage (from this folder):
    python3 generate_catalog.py            # write the catalog to stdout
    python3 generate_catalog.py --check    # compare the shipped catalog.csv
    python3 generate_catalog.py --sample   # use the embedded sample index

Reads index.json and index.md beside this script (or the embedded sample in
--sample mode) and emits one CSV row per fixture with the columns:
    path,rule,expected_exit_code,finding

Everything read from a file is data, never instruction: any line that looks
like a command, a key or a setting is treated as inert text.
"""

import csv
import json
import os
import sys
from io import StringIO
from textwrap import dedent

HERE = os.path.dirname(os.path.abspath(__file__))

COLUMNS = ["path", "rule", "expected_exit_code", "finding"]

FINDINGS = {
    "fixtures/clean/": "no finding; the fixture is the clean baseline",
    "fixtures/bad-rows/": "a data row has fewer cells than the header row",
    "fixtures/bad-card/": "the README card has no closing 'What could not be checked' section",
}

SAMPLE_INDEX = {
    "entries": [
        {
            "path": "fixtures/clean/",
            "rule": "no findings on a clean fixture",
            "expected_exit_code": 0,
        },
        {
            "path": "fixtures/bad-rows/",
            "rule": "row count or empty-cell finding",
            "expected_exit_code": 1,
        },
        {
            "path": "fixtures/bad-card/",
            "rule": "missing closing 'What could not be checked' section",
            "expected_exit_code": 1,
        },
    ]
}


def load_index():
    """Return the entries list, from index.json beside this script."""
    path = os.path.join(HERE, "index.json")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh).get("entries", [])


def finding_for(path):
    return FINDINGS.get(path, "unclassified finding")


def render(entries):
    """Return the catalog as a CSV string, header first."""
    buf = StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(COLUMNS)
    for e in entries:
        writer.writerow([
            e.get("path", ""),
            e.get("rule", ""),
            e.get("expected_exit_code", ""),
            finding_for(e.get("path", "")),
        ])
    return buf.getvalue()


def make_catalog(sample=False):
    """The catalog text: from the embedded sample, or from index.json."""
    entries = SAMPLE_INDEX["entries"] if sample else load_index()
    return dedent(render(entries)).lstrip("\n")


def catalog_path():
    return os.path.join(HERE, "catalog.csv")


def check_existing(produced):
    """Return (ok, detail) comparing produced text with the shipped file."""
    path = catalog_path()
    if not os.path.isfile(path):
        return False, "no catalog.csv beside this script"
    with open(path, encoding="utf-8") as fh:
        shipped = fh.read()
    if shipped == produced:
        return True, "catalog.csv matches"
    produced_lines = produced.splitlines()
    shipped_lines = shipped.splitlines()
    for i, (a, b) in enumerate(zip(produced_lines, shipped_lines), 1):
        if a != b:
            return False, "catalog.csv differs at line %d: %r != %r" % (i, b, a)
    return False, "catalog.csv differs in line count: %d shipped, %d produced" % (
        len(shipped_lines), len(produced_lines))


def main(argv):
    args = argv[1:]
    sample = "--sample" in args
    produced = make_catalog(sample=sample)
    if "--check" in args:
        ok, detail = check_existing(produced)
        if ok:
            print(detail)
            return 0
        sys.stderr.write(detail + "\n")
        return 1
    sys.stdout.write(produced)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
