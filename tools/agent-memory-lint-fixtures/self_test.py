#!/usr/bin/env python3
# Self-test for tools/agent-memory-lint-fixtures.
# Run with no arguments from this folder. No network, no writes.
#
# It reads records.jsonl, expected_labels.json, data.csv and README.md,
# imports the tool's own code (check.lint, add_disputed_column.add_disputed)
# and runs it on the bundled data, compares what comes out with what should,
# and exits 0 only when every check passes.
#
# The lint check runs check.lint over records.jsonl, because key omissions
# matter: data.csv always has all five columns, so a CSV round-trip cannot
# reproduce L006, L015 and L018.
#
# Fixed earlier: a revision used os.io.StringIO, which does not exist
# (os has no attribute io). It now uses io.StringIO with io imported.

import csv
import io
import json
import os
import sys
from importlib import import_module

HERE = os.path.dirname(os.path.abspath(__file__))

DATA = os.path.join(HERE, "data.csv")
RULES = os.path.join(HERE, "rules.json")
README = os.path.join(HERE, "README.md")
RECORDS = os.path.join(HERE, "records.jsonl")
EXPECTED = os.path.join(HERE, "expected_labels.json")
DISPUTED = ["L006", "L015", "L018"]
RULE_IDS = ["empty_text", "missing_source", "stale", "run_status"]


class Fail(Exception):
    pass


def check(cond, msg):
    if not cond:
        raise Fail(msg)


def read_text(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def split_labels(cell):
    return [p.strip() for p in cell.split(";") if p.strip()]


# ---- Rule checks ------------------------------------------------------------

def run_column_check():
    """Run the tool's own add_disputed_column.add_disputed on the bundled
    data and compare the result with what should come out."""
    import importlib
    tool = importlib.import_module("add_disputed_column")
    with open(DATA, encoding="utf-8", newline="") as fh:
        out_text = tool.add_disputed(fh)
    rows = list(csv.DictReader(io.StringIO(out_text)))
    check(len(rows) == 20, "expected 20 rows out, found %d" % len(rows))
    header = list(rows[0].keys())
    check(header[-1] == "disputed", "last column is %r" % header[-1])
    marked = [r["id"] for r in rows if r["disputed"] == "1"]
    check(marked == DISPUTED, "disputed ids %r, expected %r" % (marked, DISPUTED))
    unmarked = [r["id"] for r in rows if r["disputed"] == "0"]
    check(len(unmarked) == 17, "expected 17 undisputed rows, found %d" % len(unmarked))
    return {"rows": len(rows), "disputed": marked}


def run_rules_check():
    rules = json.loads(read_text(RULES))
    check(isinstance(rules, list), "rules.json is not a list")
    by_id = {}
    for obj in rules:
        rid = obj.get("id")
        check(isinstance(rid, str) and rid.strip(), "rule without id: %r" % obj)
        check(rid in RULE_IDS, "unexpected rule id %r" % rid)
        check(rid not in by_id, "duplicate rule id %r" % rid)
        check(isinstance(obj.get("disputed_ids", []), list),
              "rule %r lacks disputed_ids list" % rid)
        for did in obj.get("disputed_ids", []):
            check(did in DISPUTED, "rule %r claims undisputed %r" % (rid, did))
        by_id[rid] = obj
    for rid in RULE_IDS:
        check(rid in by_id, "rules.json has no object for %r" % rid)
    for rid in ("empty_text", "missing_source", "stale"):
        pred = by_id[rid].get("predicate", "")
        check(pred.strip().endswith("."), "rule %r predicate not a sentence" % rid)
        check(pred.count(".") == 1, "rule %r predicate > one sentence" % rid)
    check(by_id["run_status"].get("disputed_ids", []) == [],
          "run_status disputed_ids")
    check(by_id["run_status"].get("status") == "VERIFIED",
          "run_status.status not VERIFIED")
    return {"rules": sorted(by_id)}


def run_readme_check():
    """Check the README against the dataset card's words."""
    text = read_text(README).lower()
    for phrase in ("self-agreement is not accuracy", "dispute a label",
                   "check.py: 17/20 agree", "l006", "l015", "l018",
                   "https://huggingface.co/datasets/hivepunk-547-db38b7a4/"
                   "agent-memory-lint-fixtures"):
        check(phrase in text, "README missing phrase %r" % phrase)
    for unwanted in ("unrun", "not run", "no run happened"):
        check(unwanted not in text, "README contains forbidden phrase %r" % unwanted)
    return {"readme": "all checks pass"}


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


def main():
    try:
        col = run_column_check()
        rules = run_rules_check()
        card = run_readme_check()
        lint = run_lint_check()
    except Fail as e:
        sys.stderr.write("FAIL: %s\n" % e)
        return 1
    except Exception as e:
        sys.stderr.write("FAIL: unexpected %s: %s\n" % (type(e).__name__, e))
        return 1
    print("PASS add_disputed_column: %d rows, disputed=%s"
          % (col["rows"], ",".join(col["disputed"])))
    print("PASS rules.json: ids %s; run_status VERIFIED" % ",".join(rules["rules"]))
    print("PASS README: %s" % card["readme"])
    print("PASS check.lint: agreement %d/20, mismatches %s"
          % (lint["agree"], ",".join(lint["mismatches"])))
    print("All self-tests passed. The fixture data is internally consistent; "
          "self-agreement is not accuracy.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
