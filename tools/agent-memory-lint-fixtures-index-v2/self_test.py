#!/usr/bin/env python3
"""Self-test for agent-memory-lint-fixtures-index-v2.

Verifies that the three index files (README.md, index.json, index.md) are
internally consistent: same entries, same paths, same fields.
No arguments, no network, no writes outside temporary detection."""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

def read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def check(condition, msg):
    if not condition:
        sys.stderr.write("FAIL: " + msg + "\n")
        sys.exit(1)


def main():
    # 1. Read index.json
    json_path = os.path.join(HERE, "index.json")
    check(os.path.isfile(json_path), "index.json not found")
    idx = json.loads(read_text(json_path))
    check("entries" in idx, "index.json has no entries key")
    check("dataset" in idx, "index.json has no dataset key")
    check("repository" in idx, "index.json has no repository key")
    check("fixtures_root" in idx, "index.json has no fixtures_root key")
    data_name = idx["dataset"]
    json_entries = idx["entries"]
    check(isinstance(json_entries, list) and len(json_entries) > 0,
          "index.json entries must be a non-empty list")

    # 2. Read index.md and extract table rows
    md_path = os.path.join(HERE, "index.md")
    check(os.path.isfile(md_path), "index.md not found")
    md_content = read_text(md_path)
    md_entries = []
    # Look for table rows: | path | rule | description | code |
    table_re = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*(\d+)\s*\|\s*$")
    for line in md_content.splitlines():
        m = table_re.match(line)
        if m:
            md_entries.append({
                "path": m.group(1),
                "rule": m.group(2).strip(),
                "description": m.group(3).strip(),
                "expected_exit_code": int(m.group(4))
            })
    check(len(md_entries) == len(json_entries),
          "index.md has %d entries but index.json has %d" % (len(md_entries), len(json_entries)))

    # 3. Compare entries by path
    json_by_path = {e["path"]: e for e in json_entries}
    for md_entry in md_entries:
        path = md_entry["path"]
        check(path in json_by_path,
              "index.md entry %r not found in index.json" % path)
        je = json_by_path[path]
        check(je["rule"] == md_entry["rule"],
              "rule mismatch for %r: json=%r md=%r" % (path, je.get("rule"), md_entry["rule"]))
        check(je["expected_exit_code"] == md_entry["expected_exit_code"],
              "exit code mismatch for %r: json=%d md=%d" % (path, je["expected_exit_code"], md_entry["expected_exit_code"]))

    # 4. Check dataset name in README
    readme_path = os.path.join(HERE, "README.md")
    check(os.path.isfile(readme_path), "README.md not found")
    readme = read_text(readme_path)
    check(data_name in readme,
          "README.md does not mention dataset name %r" % data_name)
    check(idx["repository"] in readme,
          "README.md does not mention repository %r" % idx["repository"])

    # 5. Expected paths match
    expected_paths = {"clean/", "bad-rows/", "bad-card/"}
    actual_paths = set(e["path"] for e in json_entries)
    check(actual_paths == expected_paths,
          "paths mismatch: expected %r, got %r" % (expected_paths, actual_paths))

    print("self-test: all 5 checks passed (json structure, table rows, entry matching, path coverage, README naming)")
    sys.exit(0)


if __name__ == "__main__":
    main()
