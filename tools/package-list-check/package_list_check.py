#!/usr/bin/env python3
"""package_list_check.py: compare local files to a README '## Files' list.

Usage (from this folder):
    python3 package_list_check.py                 # check this folder
    python3 package_list_check.py /path/to/pkg    # check that folder
    python3 package_list_check.py --check /path/to/pkg

Reads only the target folder as data (no network, no publish). The
folder must contain a README.md with a '## Files' (or '## File list')
section listing file names as '- name' bullets. The local file list
is every regular file directly in the folder (subdirectories are
skipped, __pycache__/ and .git/ directories are not files anyway).

Exits 0 with 'ok: ...' when the two sets match exactly with no
duplicates, otherwise exits 1 printing one 'FAIL: ' line per
problem: listed file missing on disk, file on disk missing from
the list, duplicate entry in the list, missing folder, missing
README, or missing Files section.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
README_NAME = "README.md"
SKIP_DIRS = {"__pycache__", ".git"}


def extract_file_list(text):
    """Return (files, found_section) from the ## Files section.

    Bullet names may contain letters, digits, '.', '_', '-', '/' and
    no spaces or backticks, matching the card-check list format.
    """
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


def local_files(path):
    """Return (names, problems) for regular files directly in path."""
    if not os.path.exists(path):
        return [], ["folder not found: %s" % path]
    if not os.path.isdir(path):
        return [], ["not a folder: %s" % path]
    try:
        entries = list(os.scandir(path))
    except OSError as e:
        return [], ["could not read %s: %s: %s" % (path, type(e).__name__, e)]
    names = []
    problems = []
    for entry in entries:
        if entry.name in SKIP_DIRS:
            continue
        try:
            if entry.is_file():
                names.append(entry.name)
        except OSError as e:
            problems.append("could not stat %s: %s: %s" % (entry.name, type(e).__name__, e))
    names.sort()
    return names, problems


def _dupes(names):
    seen = set()
    dupes = set()
    for n in names:
        if n in seen:
            dupes.add(n)
        seen.add(n)
    return sorted(dupes)


def compare(listed, on_disk):
    """Return problems for duplicates, missing and extra entries.

    missing = on disk but not listed. extra = listed but not on disk.
    """
    problems = []
    dupes = _dupes(listed)
    if dupes:
        problems.append("Files list duplicate(s): %s" % ", ".join(dupes))
    listed_set = set(listed)
    disk_set = set(on_disk)
    missing = sorted(disk_set - listed_set)
    extra = [n for n in dict.fromkeys(listed) if n not in disk_set]
    if missing:
        problems.append("file(s) on disk missing from Files list: %s" % ", ".join(missing))
    if extra:
        problems.append("file(s) listed but missing on disk: %s" % ", ".join(extra))
    return problems


def verify(folder):
    """Return (ok, problems, listed, on_disk) for folder."""
    folder = os.path.abspath(folder)
    on_disk, problems = local_files(folder)
    if problems:
        return False, problems, [], on_disk
    readme = os.path.join(folder, README_NAME)
    if not os.path.isfile(readme):
        return False, ["README.md not found in %s" % folder], [], on_disk
    try:
        with open(readme, encoding="utf-8") as fh:
            text = fh.read()
    except (OSError, UnicodeError) as e:
        return False, ["could not read %s: %s: %s" % (readme, type(e).__name__, e)], [], on_disk
    listed, found = extract_file_list(text)
    problems = []
    if not found:
        problems.append("no '## Files' or '## File list' section in README.md")
    else:
        problems += compare(listed, on_disk)
    return (not problems), problems, listed, on_disk


def main(argv):
    args = [a for a in argv[1:] if a != "--check"]
    folder = os.path.abspath(args[0]) if args else HERE
    ok, problems, listed, on_disk = verify(folder)
    if ok:
        print("ok: README Files list matches local files (%s)" % ", ".join(on_disk))
        return 0
    for p in problems:
        print("FAIL: " + p)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
