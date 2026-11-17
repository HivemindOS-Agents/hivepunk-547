#!/usr/bin/env python3
"""csv_index_diff.py: compare two sorted fixtures-index-v4 CSVs.

Usage (from this folder):
    python3 csv_index_diff.py OLD.csv NEW.csv
    python3 csv_index_diff.py --check OLD.csv NEW.csv

Each CSV must have header file_name,bytes,lines and rows sorted by
file_name, as printed by fixtures-index-v4 index.py. This tool reads
both files as data only (no network, no publish, writes nothing).

It reports added (only in NEW), removed (only in OLD), changed
(in both, but bytes or lines differ), duplicate file_names within
either file, and rows out of sorted order. Exit 0 and 'ok:' only
when there is no difference of any kind; otherwise it prints one
'FAIL:' line per problem and exits 1.
"""

import csv
import os
import sys

HEADER = ["file_name", "bytes", "lines"]


def read_csv(path):
    """Return (rows, problems). rows: list of (file_name, bytes, lines).

    bytes/lines are kept as stripped strings so comparison is exact
    on the text values; blank lines are ignored.
    """
    if not os.path.exists(path):
        return [], ["not found: %s" % path]
    if not os.path.isfile(path):
        return [], ["not a file: %s" % path]
    try:
        with open(path, newline="", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            records = [r for r in reader if r and any(c.strip() for c in r)]
    except (OSError, UnicodeError, csv.Error) as e:
        return [], ["could not read %s: %s: %s" % (path, type(e).__name__, e)]
    if not records:
        return [], ["empty file, missing header: %s" % path]
    problems = []
    header = [c.strip() for c in records[0]]
    if header != HEADER:
        problems.append("bad header in %s: expected %s got %s" % (path, ",".join(HEADER), ",".join(header)))
    rows = []
    for i, rec in enumerate(records[1:], start=2):
        rec = [c.strip() for c in rec]
        if len(rec) != 3:
            problems.append("malformed row %d in %s: expected 3 fields got %d" % (i, path, len(rec)))
            continue
        if not rec[0]:
            problems.append("blank file_name at row %d in %s" % (i, path))
            continue
        rows.append(tuple(rec))
    return rows, problems


def _dupes(rows):
    seen, dupes = set(), set()
    for name, _, _ in rows:
        if name in seen:
            dupes.add(name)
        seen.add(name)
    return sorted(dupes)


def _unsorted(rows):
    names = [r[0] for r in rows]
    return names != sorted(names)


def compare(old_rows, new_rows):
    """Return (added, removed, changed, problems) lists.

    added/removed/changed are lists of file_names (changed sorted).
    problems covers duplicates and unsorted order in either input.
    First occurrence wins for changed comparison when duplicated.
    """
    problems = []
    for label, rows in (("old", old_rows), ("new", new_rows)):
        dupes = _dupes(rows)
        if dupes:
            problems.append("duplicate file_name(s) in %s: %s" % (label, ", ".join(dupes)))
        if _unsorted(rows):
            problems.append("rows not sorted by file_name in %s" % label)
    old = {}
    for r in old_rows:
        old.setdefault(r[0], r)
    new = {}
    for r in new_rows:
        new.setdefault(r[0], r)
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = sorted(n for n in set(old) & set(new) if old[n][1:] != new[n][1:])
    return added, removed, changed, problems


def diff_files(old_path, new_path):
    """Return (ok, report_lines) comparing the two CSV files."""
    old_rows, old_problems = read_csv(old_path)
    new_rows, new_problems = read_csv(new_path)
    problems = old_problems + new_problems
    if old_problems or new_problems:
        return False, problems
    added, removed, changed, dup_problems = compare(old_rows, new_rows)
    problems = list(dup_problems)
    lines = []
    for n in added:
        lines.append("added: %s" % n)
    for n in removed:
        lines.append("removed: %s" % n)
    for n in changed:
        old = next(r for r in old_rows if r[0] == n)
        new = next(r for r in new_rows if r[0] == n)
        lines.append("changed: %s old bytes=%s lines=%s new bytes=%s lines=%s" % (n, old[1], old[2], new[1], new[2]))
    lines.extend(problems)
    ok = not (added or removed or changed or problems)
    return ok, lines


def main(argv):
    args = [a for a in argv[1:] if a != "--check"]
    if len(args) != 2:
        print("FAIL: usage: python3 csv_index_diff.py OLD.csv NEW.csv")
        return 1
    ok, lines = diff_files(args[0], args[1])
    if ok:
        print("ok: no differences")
        return 0
    for line in lines:
        print("FAIL: " + line)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
