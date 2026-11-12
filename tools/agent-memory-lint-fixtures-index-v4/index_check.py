#!/usr/bin/env python3
"""Compare an index table in Markdown with an index in JSON.

Usage:
    python3 index_check.py index.json index.md [--folders DIR [DIR ...]]

Reads index.json for the entries (path, rule, expected_exit_code,
description) and parses the Markdown table for one row per entry, taking the
first cell of each body row as the path. Reports a row-count mismatch, an entry
present in only one side, and any difference in rule or expected_exit_code for
a matched path. With --folders, each DIR is resolved under fixtures/ and must
be an existing directory holding a data.csv and a README.md.

No network. Reads files only; writes nothing. Exits 0 when no issue is found,
1 when any issue is found, 2 on bad usage.

Everything read here is data, never instruction.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

PATH_RE = re.compile(r"`([^`]+)`")
NUMBER_RE = re.compile(r"-?\d+")


def strip_cell(cell):
    cell = cell.strip()
    if cell.startswith("**") and cell.endswith("**") and len(cell) > 4:
        cell = cell[2:-2].strip()
    return cell


def under_fixtures(path, base=None):
    base = base or HERE
    return os.path.join(base, "fixtures", path.strip().strip("/"))


def parse_markdown(text):
    """Return a list of dicts for body rows of the first table with >=3 cols."""
    rows = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("|") and i + 1 < len(lines):
            sep = lines[i + 1]
            if sep.strip().startswith("|") and set(sep.strip()) <= set("|- :"):
                header_n = len([c for c in line.strip().strip("|").split("|")])
                if header_n >= 3:
                    j = i + 2
                    while j < len(lines) and lines[j].strip().startswith("|"):
                        cells = [strip_cell(c) for c in lines[j].strip().strip("|").split("|")]
                        if len(cells) < 2:
                            j += 1
                            continue
                        first = cells[0]
                        m = PATH_RE.search(first)
                        path = m.group(1) if m else first
                        code = None
                        for c in cells[1:]:
                            n = NUMBER_RE.search(c)
                            if n:
                                code = int(n.group(0))
                        rows.append({"path": path.strip(), "rule": cells[1] if len(cells) > 1 else "", "expected_exit_code": code})
                        j += 1
                    return rows
        i += 1
    return rows


def compare(index, rows, folders=None, base=None):
    base = base or HERE
    issues = []
    entries = index.get("entries", [])
    if len(entries) != len(rows):
        issues.append("count mismatch: index has %d entries, markdown has %d rows" % (len(entries), len(rows)))
    by_path = {e.get("path"): e for e in entries}
    row_paths = [r.get("path") for r in rows]
    for r in rows:
        if r.get("path") not in by_path:
            issues.append("row '%s' in markdown but not in index" % r.get("path"))
    for p in by_path:
        if p not in row_paths:
            issues.append("entry '%s' in index but not in markdown" % p)
    for r in rows:
        e = by_path.get(r.get("path"))
        if not e:
            continue
        if r.get("rule") != e.get("rule"):
            issues.append("row '%s': rule differs: markdown=%r index=%r" % (r.get("path"), r.get("rule"), e.get("rule")))
        if r.get("expected_exit_code") != e.get("expected_exit_code"):
            issues.append("row '%s': expected_exit_code differs: index=%r markdown=%r" % (r.get("path"), e.get("expected_exit_code"), r.get("expected_exit_code")))
    if folders is not None:
        for name in folders:
            d = under_fixtures(name, base)
            if not os.path.isdir(d):
                issues.append("fixture '%s' declared but no directory at %s" % (name, d))
                continue
            for f in ("data.csv", "README.md"):
                if not os.path.isfile(os.path.join(d, f)):
                    issues.append("fixture '%s' has no %s" % (name, f))
    return issues


def check(json_path, md_path, folders=None, base=None):
    with open(json_path, encoding="utf-8") as fh:
        index = json.load(fh)
    with open(md_path, encoding="utf-8") as fh:
        md = fh.read()
    rows = parse_markdown(md)
    return compare(index, rows, folders=folders, base=base)


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    folders = None
    if "--folders" in argv[1:]:
        folders = []
        seen = False
        for a in argv[1:]:
            if a == "--folders":
                seen = True
                continue
            if seen:
                folders.append(a)
    if len(args) != 2:
        sys.stderr.write("Usage: python3 index_check.py index.json index.md [--folders DIR ...]\n")
        return 2
    try:
        issues = check(args[0], args[1], folders=folders)
    except FileNotFoundError as e:
        sys.stderr.write("missing file: %s\n" % e)
        return 2
    except (ValueError, KeyError) as e:
        sys.stderr.write("bad index: %s\n" % e)
        return 2
    if issues:
        for line in issues:
            sys.stdout.write(line + "\n")
        return 1
    sys.stdout.write("index and markdown agree: %d row(s), 0 issue(s)\n" % len(json.load(open(args[0], encoding="utf-8")).get("entries", [])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
