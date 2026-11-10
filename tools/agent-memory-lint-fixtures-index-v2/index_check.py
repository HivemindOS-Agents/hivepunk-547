#!/usr/bin/env python3
"""index_check.py -- the checker behind agent-memory-lint-fixtures-index-v2.

Stdlib only. No network, no writes, no arguments.

Three functions:

  load_index(path)      -> the parsed JSON object at path
  parse_index_md(text)  -> one dict per data row of the markdown table in text
  compare(index, rows)  -> a list of issue strings; empty when the two agree

The markdown table this reads is the four-column one:

  | path | rule | description | expected_exit_code |

with the path cell wrapped in backticks. Headings, prose, the header row and
the '---' separator line are ignored.
"""

import json
import re

# The fields every entry and row must carry, in the order the table lists them.
FIELDS = ("path", "rule", "description", "expected_exit_code")
TEXT_FIELDS = ("rule", "description")

# | `path` | rule | description | 0 |
_ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|([^|]*)\|([^|]*)\|\s*(\d+)\s*\|\s*$")


def _squash(value):
    """Collapse every run of whitespace so a wrapped sentence equals the same
    sentence unwrapped, and a non-string becomes a comparable string."""
    if not isinstance(value, str):
        value = "" if value is None else str(value)
    return " ".join(value.split())


def load_index(path):
    """Return the parsed JSON object at path. Raises on a missing file or
    malformed JSON; the caller decides what to do about that."""
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def parse_index_md(text):
    """Return one dict per data row of the four-column markdown table."""
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


def compare(index, rows):
    """Compare a parsed JSON index with the rows read from the markdown.

    Returns a list of human-readable issue strings. An empty list means the two
    readings agree. Every issue about a specific row names that row's path.
    """
    issues = []

    if not isinstance(index, dict):
        return ["index is not a JSON object"]

    entries = index.get("entries")
    if not isinstance(entries, list):
        return ["index has no 'entries' list"]

    # --- read the JSON side -------------------------------------------------
    by_path = {}
    for i, entry in enumerate(entries):
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
        by_path[path] = entry
        for field in FIELDS[1:]:
            if field not in entry:
                issues.append("entry %r is missing %r" % (path, field))

    # --- read the markdown side --------------------------------------------
    row_by_path = {}
    for row in rows:
        path = row.get("path")
        if path in row_by_path:
            issues.append("duplicate path %r in markdown rows" % path)
            continue
        row_by_path[path] = row

    # --- counts -------------------------------------------------------------
    if len(entries) != len(rows):
        issues.append(
            "count mismatch: index has %d entries, markdown has %d rows"
            % (len(entries), len(rows)))

    # --- paths present on only one side ------------------------------------
    for path in sorted(set(row_by_path) - set(by_path)):
        issues.append("row %r appears in markdown but not in the index" % path)
    for path in sorted(set(by_path) - set(row_by_path)):
        issues.append("entry %r appears in the index but not in the markdown" % path)

    # --- field-by-field comparison on shared paths -------------------------
    for path in sorted(set(by_path) & set(row_by_path)):
        entry = by_path[path]
        row = row_by_path[path]
        for field in FIELDS[1:]:
            if field not in entry or field not in row:
                continue
            left = entry[field]
            right = row[field]
            if field == "expected_exit_code":
                if left != right:
                    issues.append(
                        "row %r: expected_exit_code differs: index=%r markdown=%r"
                        % (path, left, right))
            elif _squash(left) != _squash(right):
                issues.append(
                    "row %r: %s differs: index=%r markdown=%r"
                    % (path, field, _squash(left), _squash(right)))

    return issues
