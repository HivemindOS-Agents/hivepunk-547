#!/usr/bin/env python3
import json
import os
import sys
from importlib import import_module

# --- constants ---
HERE = os.path.abspath(os.path.dirname(__file__))

DATA = os.path.join(HERE, "data.csv")
RULES = os.path.join(HERE, "rules.json")
README = os.path.join(HERE, "README.md")
RECORDS = os.path.join(HERE, "records.jsonl")
EXPECTED = os.path.join(HERE, "expected_labels.json")
DISPUTED = ["L006", "L015", "L018"]
RULE_IDS = ["empty_text", "missing_source", "stale", "run_status"]

# --- helpers ---

def read_text(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()

def check(condition, msg):
    if not condition:
        sys.stderr.write("FAIL: " + msg + "\n")
        sys.exit(1)

# --- lint check ---

def run_lint_check():
    # Run check.lint on records.jsonl (key omissions matter for "fields").
    # data.csv always has all five columns, so it cannot reproduce L006/L015/L018.
    check(os.path.isfile(RECORDS), "missing records.jsonl")
    check(os.path.isfile(EXPECTED), "missing expected_labels.json")
    checker = import_module("check")
    expected = json.loads(read_text(EXPECTED))
    agree = 0
    mismatches = []
    for line in read_text(RECORDS).splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        rid = rec["id"]
        got = checker.lint(rec)
        if got == expected[rid]:
            agree += 1
        else:
            mismatches.append(rid)
    check(agree == 17, "agreement %d/20, expected 17" % agree)
    check(mismatches == DISPUTED, "mismatches %r, expected %r" % (mismatches, DISPUTED))
    return {"agree": agree, "mismatches": mismatches}

# --- entry point ---

def main():
    res = run_lint_check()
    print("PASS check.lint: agreement %d/20, mismatches %s" % (res["agree"], ",".join(res["mismatches"])) )
    sys.exit(0)

if __name__ == "__main__":
    main()
