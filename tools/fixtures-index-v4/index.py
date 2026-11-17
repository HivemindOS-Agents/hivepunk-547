#!/usr/bin/env python3
"""index.py: print a CSV index of regular files directly in a directory.

Usage (from this folder):
    python3 index.py                 # index this folder
    python3 index.py /path/to/dir    # index that directory
    python3 index.py --check /path/to/dir

Reads only the named directory as data (no network, no publish).
Prints to stdout a CSV with header file_name,bytes,lines and one row
per regular file directly in the directory (subdirectories are
skipped), sorted by file_name. bytes is the file size in bytes.
lines is the line count for .py/.md/.csv/.txt/.json files
(case-insensitive) and blank for all other files.

Exit 0 on success; exit 1 and print a FAIL line otherwise (missing
path, not a directory, unreadable file).
"""

import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEXT_EXTENSIONS = {".py", ".md", ".csv", ".txt", ".json"}
HEADER = ["file_name", "bytes", "lines"]


def count_lines(path):
    """Return the number of lines in a text file.

    Lines are counted on raw bytes: one per newline, plus one for a
    final line without a trailing newline. An empty file has 0 lines.
    """
    with open(path, "rb") as fh:
        data = fh.read()
    if not data:
        return 0
    count = data.count(b"\n")
    if not data.endswith(b"\n"):
        count += 1
    return count


def index_directory(path):
    """Return (rows, problems) for regular files directly in path.

    rows is a list of (file_name, bytes, lines_or_None) sorted by
    file_name. problems is a list of strings (empty on success).
    """
    if not os.path.exists(path):
        return [], ["not found: %s" % path]
    if not os.path.isdir(path):
        return [], ["not a directory: %s" % path]
    try:
        entries = list(os.scandir(path))
    except OSError as e:
        return [], ["could not read %s: %s: %s" % (path, type(e).__name__, e)]
    rows = []
    problems = []
    for entry in entries:
        try:
            if not entry.is_file():
                continue
        except OSError as e:
            problems.append("could not stat %s: %s: %s" % (entry.name, type(e).__name__, e))
            continue
        ext = os.path.splitext(entry.name)[1].lower()
        try:
            size = entry.stat().st_size
            lines = count_lines(entry.path) if ext in TEXT_EXTENSIONS else None
        except OSError as e:
            problems.append("could not read %s: %s: %s" % (entry.name, type(e).__name__, e))
            continue
        rows.append((entry.name, size, lines))
    rows.sort(key=lambda r: r[0])
    return rows, problems


def render_csv(rows):
    """Return the CSV text for rows, including the header."""
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(HEADER)
    for name, size, lines in rows:
        writer.writerow([name, size, "" if lines is None else lines])
    return buf.getvalue()


def verify(path):
    """Return (ok, problems, rows)."""
    rows, problems = index_directory(path)
    return (not problems), problems, rows


def main(argv):
    args = [a for a in argv[1:] if a != "--check"]
    path = os.path.abspath(args[0]) if args else HERE
    ok, problems, rows = verify(path)
    if not ok:
        for p in problems:
            print("FAIL: " + p)
        return 1
    sys.stdout.write(render_csv(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
