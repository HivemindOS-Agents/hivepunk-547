#!/usr/bin/env python3
"""csv_files.py: print a Markdown Files list from a CSV file_name column.

Usage (from this folder):
    python3 csv_files.py                 # read data.csv beside this file
    python3 csv_files.py PATH.csv        # read PATH.csv
    python3 csv_files.py --check PATH.csv

Reads only the CSV as data (no network, no publish). Handles normal
quoted CSV quoting via the csv module (e.g. a quoted name containing a
comma) and skips fully blank rows. Prints to stdout a Markdown list in
the card-check format: a '## Files' heading followed by one '- name'
bullet per file_name value, in CSV order.

Exit 0 on success; exit 1 and print one problem per line prefixed
'FAIL: ' otherwise (missing file, missing file_name column, empty
file_name in a non-blank row, duplicate file_name, or no values).
"""

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.join(HERE, "data.csv")


def read_names(path):
    """Return (names, problems) for the file_name column of the CSV."""
    if not os.path.isfile(path):
        return [], ["file not found: %s" % path]
    try:
        with open(path, encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames is None or "file_name" not in reader.fieldnames:
                return [], ["data.csv has no file_name column (header %r)"
                            % (reader.fieldnames,)]
            names = []
            problems = []
            for lineno, row in enumerate(reader, start=2):
                if row is None:
                    continue
                values = list(row.values())
                if all(v is None or str(v).strip() == "" for v in values):
                    continue  # fully blank row: skip it
                name = (row.get("file_name") or "").strip()
                if not name:
                    problems.append("row %d: empty file_name" % lineno)
                    continue
                names.append(name)
    except (OSError, csv.Error, UnicodeError) as e:
        return [], ["could not read %s: %s: %s" % (path, type(e).__name__, e)]
    seen = set()
    dupes = []
    for n in names:
        if n in seen:
            dupes.append(n)
        seen.add(n)
    if dupes:
        problems.append("duplicate file_name(s): %s"
                        % ", ".join(sorted(set(dupes))))
    if not names and not problems:
        problems.append("no file_name values found in %s" % path)
    return names, problems


def render_markdown(names):
    """Return the card-check-format Markdown Files list for names."""
    lines = ["## Files", ""]
    lines.extend("- %s" % n for n in names)
    return "\n".join(lines) + "\n"


def verify(path):
    """Return (ok, problems, names)."""
    names, problems = read_names(path)
    return (not problems), problems, names


def main(argv):
    args = [a for a in argv[1:] if a != "--check"]
    path = os.path.abspath(args[0]) if args else DEFAULT_CSV
    ok, problems, names = verify(path)
    if not ok:
        for p in problems:
            print("FAIL: " + p)
        return 1
    sys.stdout.write(render_markdown(names))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
