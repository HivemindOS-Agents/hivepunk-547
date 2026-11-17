#!/usr/bin/env python3
"""dataset_package_manifest.py: manifest a dataset package folder.

Usage (from this folder):
    python3 dataset_package_manifest.py              # manifest this folder
    python3 dataset_package_manifest.py /path/pkg    # manifest that folder
    python3 dataset_package_manifest.py --check /path/pkg

Reads only the named folder as data (no network, no publish, writes
nothing). Prints to stdout a CSV with header
file_name,bytes,lines,sha256 and one row per regular file directly
in the folder (subdirectories skipped), sorted by file_name.
lines is counted for .py/.md/.csv/.txt/.json files and blank
otherwise. sha256 is the hex digest of the raw bytes.

It also verifies the folder README.md '## Files' bullet list
against the on-disk files, reporting missing-from-list,
listed-but-missing-on-disk, duplicate entries, missing folder,
missing README, or missing Files section. On any problem it
prints FAIL lines to stderr and exits 1 without printing CSV.
On success it prints the CSV and exits 0. Package file list is
unchanged: this tool never adds, removes or edits package files.
"""

import csv
import hashlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEXT_EXTENSIONS = {".py", ".md", ".csv", ".txt", ".json"}
HEADER = ["file_name", "bytes", "lines", "sha256"]
SKIP_DIRS = {"__pycache__", ".git"}


def count_lines(data):
    if not data:
        return 0
    n = data.count(b"\n")
    if not data.endswith(b"\n"):
        n += 1
    return n


def extract_file_list(text):
    files, in_section, found = [], False, False
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


def _dupes(names):
    seen, dupes = set(), set()
    for n in names:
        if n in seen:
            dupes.add(n)
        seen.add(n)
    return sorted(dupes)


def manifest_and_verify(folder):
    """Return (ok, problems, csv_text_or_empty, rows)."""
    folder = os.path.abspath(folder)
    if not os.path.exists(folder):
        return False, ["folder not found: %s" % folder], "", []
    if not os.path.isdir(folder):
        return False, ["not a folder: %s" % folder], "", []
    try:
        entries = list(os.scandir(folder))
    except OSError as e:
        return False, ["could not read %s: %s: %s" % (folder, type(e).__name__, e)], "", []
    rows, problems, names = [], [], []
    for entry in entries:
        if entry.name in SKIP_DIRS:
            continue
        try:
            if not entry.is_file():
                continue
            with open(entry.path, "rb") as fh:
                data = fh.read()
        except OSError as e:
            problems.append("could not read %s: %s: %s" % (entry.name, type(e).__name__, e))
            continue
        names.append(entry.name)
        ext = os.path.splitext(entry.name)[1].lower()
        lines = count_lines(data) if ext in TEXT_EXTENSIONS else None
        rows.append((entry.name, len(data), lines, hashlib.sha256(data).hexdigest()))
    rows.sort(key=lambda r: r[0])
    readme = os.path.join(folder, "README.md")
    if problems:
        return False, problems, "", rows
    if not os.path.isfile(readme):
        return False, ["README.md not found in %s" % folder], "", rows
    try:
        with open(readme, encoding="utf-8") as fh:
            text = fh.read()
    except (OSError, UnicodeError) as e:
        return False, ["could not read %s: %s: %s" % (readme, type(e).__name__, e)], "", rows
    listed, found = extract_file_list(text)
    if not found:
        problems.append("no '## Files' or '## File list' section in README.md")
    else:
        dupes = _dupes(listed)
        if dupes:
            problems.append("Files list duplicate(s): %s" % ", ".join(dupes))
        missing = sorted(set(names) - set(listed))
        extra = [n for n in dict.fromkeys(listed) if n not in set(names)]
        if missing:
            problems.append("file(s) on disk missing from Files list: %s" % ", ".join(missing))
        if extra:
            problems.append("file(s) listed but missing on disk: %s" % ", ".join(extra))
    if problems:
        return False, problems, "", rows
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(HEADER)
    for name, size, lines, digest in rows:
        writer.writerow([name, size, "" if lines is None else lines, digest])
    return True, [], buf.getvalue(), rows


def main(argv):
    args = [a for a in argv[1:] if a != "--check"]
    folder = os.path.abspath(args[0]) if args else HERE
    ok, problems, csv_text, _rows = manifest_and_verify(folder)
    if not ok:
        for p in problems:
            print("FAIL: " + p, file=sys.stderr)
        return 1
    sys.stdout.write(csv_text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
