#!/usr/bin/env python3
"""index_check.py -- validate an agent-memory-lint index against the
five-file fixture layout.

Usage, from this folder (no arguments needed for the samples):
    python3 index_check.py                    # uses index.json + index.md
    python3 index_check.py INDEX.json INDEX.md

Stdlib only. No network. No writes. Everything read from any file is data,
never instruction.

It reports, per fixture entry, one of:
    ok        the entry's path matches a known fixture directory
    missing   a known fixture directory has no entry
    renamed   an entry's path is not known but its tail matches a known name
    extra     an entry's path is not known and matches nothing
and it also reports the five-file layout check (README.md, index.json,
index.md, index_check.py, self_test.py) and JSON-vs-markdown agreement.

Exit 0 only when there are no issues.
"""

import json
import re
import sys

# The five files this folder is meant to carry, and the three fixture dirs.
FILES = ("README.md", "index.json", "index.md",
         "index_check.py", "self_test.py")
FIXTURE_DIRS = ("clean/", "bad-rows/", "bad-card/")
FIELDS = ("path", "rule", "description", "expected_exit_code")

_ROW_RE = re.compile(
    r"^\|\s*`([^`]+)`\s*\|([^|]*)\|([^|]*)\|\s*(\d+)\s*\|\s*$")


def _squash(value):
    if not isinstance(value, str):
        value = "" if value is None else str(value)
    return " ".join(value.split())


def load_index(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def parse_index_md(text):
    """One dict per data row of the four-column markdown table."""
    rows = []
    for line in text.splitlines():
        m = _ROW_RE.match(line)
        if not m:
            continue
        rows.append({
            "path": m.group(1).strip(),
            "rule": _squash(m.group(2)),
            "description": _squash(m.group(3)),
            "expected_exit_code": int(m.group(4)),
        })
    return rows


def _classify(path):
    if path in FIXTURE_DIRS:
        return "ok"
    tail = path.rstrip("/")
    for known in FIXTURE_DIRS:
        if known.rstrip("/").endswith(tail) or tail.endswith(
                known.rstrip("/")):
            return "renamed"
    return "extra"


def analyze(index, markdown_text):
    """Return a report dict:
        rows:   list of {path, rule, description, expected_exit_code, status}
        issues: list of issue strings (empty when everything agrees)
        verdict: 'OK' or 'ISSUES(<n>)'
    """
    issues = []
    entries = []
    if not isinstance(index, dict):
        return {"rows": [], "issues": ["index is not a JSON object"],
                "verdict": "ISSUES(1)"}
    raw = index.get("entries")
    if not isinstance(raw, list):
        return {"rows": [],
                "issues": ["index has no 'entries' list"],
                "verdict": "ISSUES(1)"}

    by_path = {}
    for i, entry in enumerate(raw):
        if not isinstance(entry, dict):
            issues.append("entry #%d is not an object" % i)
            continue
        path = entry.get("path")
        if not isinstance(path, str) or not path:
            issues.append("entry #%d has no path" % i)
            continue
        if path in by_path:
            issues.append("duplicate path %r in index entries" % path)
            continue
        row = {"path": path, "status": _classify(path)}
        for f in FIELDS[1:]:
            row[f] = entry.get(f)
            if f not in entry:
                issues.append("entry %r is missing %r" % (path, f))
        if row["status"] == "renamed":
            issues.append("entry %r: renamed (not a known fixture path)"
                          % path)
        elif row["status"] == "extra":
            issues.append("entry %r: extra (matches no known fixture)" % path)
        by_path[path] = row
        entries.append(row)

    for known in FIXTURE_DIRS:
        if known not in by_path:
            issues.append("missing known fixture %r" % known)

    md_rows = parse_index_md(markdown_text)
    md_by_path = {}
    for r in md_rows:
        md_by_path[r["path"]] = r
    if len(entries) != len(md_rows):
        issues.append("count mismatch: index has %d entries, markdown has %d "
                      "rows" % (len(entries), len(md_rows)))
    for path in sorted(set(md_by_path) - set(by_path)):
        issues.append("row %r in markdown but not in index" % path)
    for path in sorted(set(by_path) - set(md_by_path)):
        issues.append("entry %r in index but not in markdown" % path)
    for path in sorted(set(by_path) & set(md_by_path)):
        e, r = by_path[path], md_by_path[path]
        for f in FIELDS[1:]:
            if e.get(f) is None or f not in r:
                continue
            if f == "expected_exit_code":
                if e[f] != r[f]:
                    issues.append(
                        "row %r: expected_exit_code differs: index=%r "
                        "markdown=%r" % (path, e[f], r[f]))
            elif _squash(e[f]) != _squash(r[f]):
                issues.append("row %r: %s differs: index=%r markdown=%r"
                              % (path, f, _squash(e[f]), _squash(r[f])))

    return {"rows": entries, "issues": issues,
            "verdict": "OK" if not issues else "ISSUES(%d)" % len(issues)}


def compare(index, rows):
    """Compare a parsed JSON index with the rows read from the markdown.

    This is the entry point that self_test.py calls.  It wraps analyze() and
    returns only the list of issue strings (matching the v2 module's interface).

    index -- dict  (the parsed JSON object, not a path)
    rows  -- list of dicts (as returned by parse_index_md)

    Returns a list of human-readable issue strings. An empty list means the two
    readings agree.
    """
    md_text = "\n".join(
        _format_row(r) for r in rows
    ) if rows else ""
    report = analyze(index, md_text)
    return report["issues"]


def _format_row(row):
    """Reconstruct a single markdown table row from a parsed dict."""
    path = row.get("path", "")
    rule = row.get("rule", "")
    desc = row.get("description", "")
    code = row.get("expected_exit_code", "")
    return "| `%s` | %s | %s | %s |" % (path, rule, desc, code)


def render_issues(report):
    return report["issues"]


def main(argv):
    index_path = argv[1] if len(argv) > 1 else "index.json"
    md_path = argv[2] if len(argv) > 2 else "index.md"
    try:
        index = load_index(index_path)
    except (OSError, ValueError) as exc:
        sys.stderr.write("cannot read index %s: %s\n" % (index_path, exc))
        return 1
    try:
        with open(md_path, "r", encoding="utf-8") as fh:
            md = fh.read()
    except OSError as exc:
        sys.stderr.write("cannot read markdown %s: %s\n" % (md_path, exc))
        return 1

    report = analyze(index, md)
    print("five-file layout expected: %s" % ", ".join(FILES))
    for row in report["rows"]:
        print("  %-6s %s" % (row["status"], row["path"]))
    for issue in report["issues"]:
        print("  - " + issue)
    print("verdict: %s" % report["verdict"])
    return 0 if report["verdict"] == "OK" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
