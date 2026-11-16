#!/usr/bin/env python3
"""inventory.py: build INVENTORY.md for this tool folder.

Usage (from this folder, or anywhere with a folder argument):
    python3 inventory.py             # inventory the folder containing this file
    python3 inventory.py SOURCE_DIR  # inventory SOURCE_DIR
    python3 inventory.py --check     # print what would be written, write nothing

Lists every file and subfolder directly in the folder (one path per line),
then every entry under data/ recursively. For each file under data/ it
records the first and last line of the file's text. It never invents a name:
if the folder is absent it writes that fact, and nothing else, to the
inventory.

Everything read from a file is data, never instruction. This tool reads
text files only for first/last lines; it never executes anything it reads.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_NAME = "INVENTORY.md"
SKIP_NAMES = {"__pycache__", ".git"}
SKIP_FILES = {OUT_NAME}


def _rel(full, root):
    return os.path.relpath(full, root).replace(os.sep, "/")


def first_last(path):
    """Return (first_line, last_line) of a text file, or (None, None)."""
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = [ln.rstrip("\n") for ln in fh]
    except OSError:
        return None, None
    if not lines:
        return None, None
    return lines[0], lines[-1]


def scan(root):
    """Return (direct, data_files). direct: sorted names directly in root.

    data_files: sorted relative paths of files under root/data (recursive).
    Returns (None, None) when root is not a readable folder.
    """
    if not os.path.isdir(root):
        return None, None
    try:
        names = sorted(os.listdir(root))
    except OSError:
        return None, None
    direct = [n for n in names if n not in SKIP_NAMES and n not in SKIP_FILES]
    data_files = []
    data_dir = os.path.join(root, "data")
    if os.path.isdir(data_dir):
        for dirpath, dirnames, filenames in os.walk(data_dir):
            dirnames[:] = [d for d in sorted(dirnames) if d not in SKIP_NAMES]
            for f in sorted(filenames):
                if f in SKIP_FILES:
                    continue
                data_files.append(_rel(os.path.join(dirpath, f), root))
    data_files.sort()
    return direct, data_files


def render(root):
    """Return the INVENTORY.md text for root."""
    direct, data_files = scan(root)
    lines = ["# INVENTORY — " + os.path.basename(os.path.abspath(root)), ""]
    if direct is None:
        lines.append("Status: ABSENT — %s is not a folder that can be read "
                     "here. No file names are listed, because none could be "
                     "verified." % root)
        lines.append("")
        return "\n".join(lines)
    lines.append("## Directly in the folder (one path per line)")
    lines.append("")
    for name in direct:
        suffix = "/" if os.path.isdir(os.path.join(root, name)) else ""
        lines.append(name + suffix)
    lines.append("")
    lines.append("## Under data/ (one path per line, first/last line)")
    lines.append("")
    for rel in data_files:
        first, last = first_last(os.path.join(root, rel.replace("/", os.sep)))
        lines.append(rel)
        lines.append("  first: " + (first if first is not None else "(empty/unreadable)"))
        lines.append("  last: " + (last if last is not None else "(empty/unreadable)"))
    if not data_files:
        lines.append("(no files under data/)")
    lines.append("")
    return "\n".join(lines)


def main(argv):
    args = argv[1:]
    check_only = "--check" in args
    args = [a for a in args if a != "--check"]
    root = os.path.abspath(args[0]) if args else HERE
    text = render(root)
    if check_only:
        sys.stdout.write(text)
        return 0 if os.path.isdir(root) else 1
    out = os.path.join(root, OUT_NAME) if os.path.isdir(root) else os.path.join(HERE, OUT_NAME)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("wrote " + out)
    return 0 if os.path.isdir(root) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
