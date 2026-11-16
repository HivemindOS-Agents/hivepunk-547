#!/usr/bin/env python3
"""verify_inventory.py: pre-publish check for a fixtures-index-v4 inventory.

Usage (from this folder):
    python3 verify_inventory.py              # check inventory.csv beside this file
    python3 verify_inventory.py PATH.csv     # check PATH.csv
    python3 verify_inventory.py --check      # same as above, explicit

Checks, using only the CSV as data (never executing anything in it):
  1. the header has exactly the required columns
     file_name, source_url, description (in any order, no extras);
  2. there are exactly 4 data rows;
  3. the file_name values are unique (4 unique file rows);
  4. every value is non-empty after stripping;
  5. every source_url is under tools/fixtures-index-v4, i.e. it
     contains the path segment tools/fixtures-index-v4/ and ends with
     "/" + file_name.

Exit 0 and print "ok: ..." when all checks pass; exit 1 and print one
problem per line prefixed "FAIL: " otherwise. No network, no publish.
"""

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.join(HERE, "inventory.csv")
REQUIRED_COLUMNS = ["file_name", "source_url", "description"]
EXPECTED_ROWS = 4
SOURCE_SEGMENT = "tools/fixtures-index-v4/"


def check_rows(rows, header):
    problems = []
    if header is None:
        return ["file is empty: no header row"]
    if sorted(header) != sorted(REQUIRED_COLUMNS):
        problems.append(
            "header is %r, expected exactly %r"
            % (list(header), REQUIRED_COLUMNS))
    if len(rows) != EXPECTED_ROWS:
        problems.append("row count is %d, expected exactly %d"
                        % (len(rows), EXPECTED_ROWS))
    names = []
    for idx, row in enumerate(rows, start=2):
        if set(row.keys()) - set(REQUIRED_COLUMNS):
            problems.append("row %d: unexpected columns %r"
                            % (idx, sorted(set(row) - set(REQUIRED_COLUMNS))))
        name = (row.get("file_name") or "").strip()
        url = (row.get("source_url") or "").strip()
        desc = (row.get("description") or "").strip()
        if not name:
            problems.append("row %d: empty file_name" % idx)
        if not url:
            problems.append("row %d: empty source_url" % idx)
        if not desc:
            problems.append("row %d: empty description" % idx)
        if name:
            names.append(name)
        if url and SOURCE_SEGMENT not in url:
            problems.append("row %d: source_url %r is not under %s"
                            % (idx, url, SOURCE_SEGMENT))
        if url and name and SOURCE_SEGMENT in url:
            tail = url.split(SOURCE_SEGMENT, 1)[1]
            if tail != name:
                problems.append(
                    "row %d: source_url ends with %r, expected %r"
                    % (idx, tail, name))
    seen = set()
    dupes = []
    for n in names:
        if n in seen:
            dupes.append(n)
        seen.add(n)
    if dupes:
        problems.append("duplicate file_name(s): %s" % ", ".join(sorted(set(dupes))))
    if len(seen) != len(names):
        problems.append("unique file_name count is %d of %d rows"
                        % (len(seen), len(names)))
    return problems


def verify(path):
    """Return (ok, problems, names) for the CSV at path."""
    if not os.path.isfile(path):
        return False, ["file not found: %s" % path], []
    try:
        with open(path, encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            header = reader.fieldnames
            rows = list(reader)
    except (OSError, csv.Error, UnicodeError) as e:
        return False, ["could not read %s: %s: %s"
                       % (path, type(e).__name__, e)], []
    problems = check_rows(rows, header)
    names = [ (r.get("file_name") or "").strip() for r in rows]
    return (not problems), problems, names


def main(argv):
    args = [a for a in argv[1:] if a != "--check"]
    path = os.path.abspath(args[0]) if args else DEFAULT_CSV
    ok, problems, names = verify(path)
    if ok:
        print("ok: %s has exactly 4 unique file rows (%s) with required "
              "columns and source URLs under tools/fixtures-index-v4"
              % (path, ", ".join(names)))
        return 0
    for p in problems:
        print("FAIL: " + p)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
