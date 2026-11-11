#!/usr/bin/env python3
"""Self-test for agent-memory-lint-fixtures-index-v3.

Runs this folder's own checker (index_check) on three inputs and prints raw
pass/fail output:
  1. sample_index.json + sample_index.md  -> 0 issues, verdict OK
  2. sample_bad_index.json + sample_index.md -> issues, one naming the
     renamed path 'bad-rows-v2/', plus an extra-entry issue
  3. this folder's own index.json + index.md -> 0 issues

Exits 0 only when every check passes. Stdlib only: no arguments, no network,
no writes. Its own run log is written by HivemindOS as SELFTEST_OUTPUT.md.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import index_check


def read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def run_case(label, index_path, md_path, want_ok):
    index = index_check.load_index(os.path.join(HERE, index_path))
    md = read_text(os.path.join(HERE, md_path))
    report = index_check.analyze(index, md)
    issues = index_check.render_issues(report)
    print("case %s: %d entr(y/ies), %d issue(s), verdict=%s"
          % (label, len(report["rows"]), len(issues), report["verdict"]))
    for line in issues:
        print("    - " + line)
    return report, issues


def main():
    failures = []

    clean_report, clean_issues = run_case(
        "clean sample", "sample_index.json", "sample_index.md", True)
    if clean_issues:
        failures.append("clean sample: expected 0 issues, got %d"
                        % len(clean_issues))
    if clean_report["verdict"] != "OK":
        failures.append("clean sample: expected verdict OK, got %s"
                        % clean_report["verdict"])

    bad_report, bad_issues = run_case(
        "bad sample", "sample_bad_index.json", "sample_index.md", False)
    if not bad_issues:
        failures.append("bad sample: expected at least 1 issue, got 0")
    if not any("bad-rows-v2" in i or "renamed" in i for i in bad_issues):
        failures.append("bad sample: no issue names the renamed path "
                        "bad-rows-v2 or reports a rename")
    if not any("extra" in i for i in bad_issues):
        failures.append("bad sample: no extra-entry issue reported")
    renamed = any(r["status"] == "renamed" for r in bad_report["rows"])
    if not renamed:
        failures.append("bad sample: no entry marked status=renamed")

    own_report, own_issues = run_case(
        "this folder", "index.json", "index.md", True)
    if own_issues:
        failures.append("this folder: expected 0 issues, got %d"
                        % len(own_issues))

    if failures:
        for line in failures:
            sys.stderr.write("FAIL: " + line + "\n")
        return 1

    print("self-test: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
