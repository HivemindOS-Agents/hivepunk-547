#!/usr/bin/env python3
"""sync_check.py: compare data.csv file_name column to README Files list.

Usage (from this folder):
    python3 sync_check.py
    python3 sync_check.py README.md data.csv
    python3 sync_check.py --check README.md data.csv

Reads files only as data (no network, no publish). The README must have
a '## Files' (or '## File list') section listing file names as
'- name' bullets; data.csv must have a file_name column. Exits 0 with
'ok: ...' when the two sets match exactly, otherwise exits 1 listing
FAIL lines for missing entries (in CSV, not in card), extra entries
(in card, not in CSV), and duplicate entries on either side.
Defaults: README.md and data.csv beside this file.
"""

import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_README = os.path.join(HERE, "README.md")
DEFAULT_CSV = os.path.join(HERE, "data.csv")


def extract_file_list(text):
    """Return (files, found_section) from the ## Files section."""
    files = []
    in_section = False
    found = False
    for line in text.splitlines():
        heading = re.match(r"^##\s+(.+?)\s*$", line.strip())
        if heading:
            in_section = heading.group(1).strip().lower() in ("files", "file list")
            if in_section:
                found = True
            continue
        if in_section:
            m = re.match(r"^\s*[-*]\s+`?([^`\s]+)`?\s*$", line)
            if m:
                files.append(m.group(1).strip())
    return files, found


def read_csv_names(path):
    """Return (names, problems) for the file_name column."""
    if not os.path.isfile(path):
        return [], ["file not found: %s" % path]
    try:
        with open(path, encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames is None or "file_name" not in reader.fieldnames:
                return [], ["data.csv has no file_name column (header %r)" % (reader.fieldnames,)]
            names = []
            problems = []
            for lineno, row in enumerate(reader, start=2):
                if row is None:
                    continue
                if all(v is None or str(v).strip() == "" for v in row.values()):
                    continue
                name = (row.get("file_name") or "").strip()
                if not name:
                    problems.append("data.csv row %d: empty file_name" % lineno)
                    continue
                names.append(name)
    except (OSError, csv.Error, UnicodeError) as e:
        return [], ["could not read %s: %s: %s" % (path, type(e).__name__, e)]
    if not names and not problems:
        problems.append("data.csv has no file_name values")
    return names, problems


def _dupes(names):
    return sorted({n for n in names if names.count(n) > 1})


def compare(listed, csv_names):
    """Return problems describing duplicates, missing and extra."""
    problems = []
    for label, names in (("data.csv", csv_names), ("file list", listed)):
        dupes = _dupes(names)
        if dupes:
            problems.append("%s duplicate(s): %s" % (label, ", ".join(dupes)))
    missing = [n for n in dict.fromkeys(csv_names) if n not in listed]
    extra = [n for n in dict.fromkeys(listed) if n not in csv_names]
    if missing:
        problems.append("file list missing from card: %s" % ", ".join(missing))
    if extra:
        problems.append("file list has extra names not in data.csv: %s" % ", ".join(extra))
    return problems


def verify(readme_path, csv_path):
    """Return (ok, problems, listed, csv_names)."""
    if not os.path.isfile(readme_path):
        return False, ["file not found: %s" % readme_path], [], []
    try:
        with open(readme_path, encoding="utf-8") as fh:
            text = fh.read()
    except (OSError, UnicodeError) as e:
        return False, ["could not read %s: %s: %s" % (readme_path, type(e).__name__, e)], [], []
    listed, found = extract_file_list(text)
    problems = []
    if not found:
        problems.append("no '## Files' or '## File list' section in README")
    csv_names, csv_problems = read_csv_names(csv_path)
    problems += csv_problems
    if csv_names and found:
        problems += compare(listed, csv_names)
    return (not problems), problems, listed, csv_names


def main(argv):
    args = [a for a in argv[1:] if a != "--check"]
    readme = os.path.abspath(args[0]) if len(args) > 0 else DEFAULT_README
    csv_path = os.path.abspath(args[1]) if len(args) > 1 else DEFAULT_CSV
    ok, problems, listed, csv_names = verify(readme, csv_path)
    if ok:
        print("ok: README Files list matches data.csv file_name column (%s)" % ", ".join(csv_names))
        return 0
    for p in problems:
        print("FAIL: " + p)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
