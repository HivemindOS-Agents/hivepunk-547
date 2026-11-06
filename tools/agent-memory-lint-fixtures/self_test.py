#!/usr/bin/env python3
# Self-test for tools/agent-memory-lint-fixtures.
# Run with NO arguments, from this folder. No network, no writes.
# Imports the tool's own code (add_disputed_column.add_disputed, check.lint)
# and compares outcomes with expected_labels in data.csv.
# Exit 0 only when every check passes.

import csv
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data.csv")
RULES = os.path.join(HERE, "rules.json")
README = os.path.join(HERE, "README.md")
DISPUTED = ["L006", "L015", "L018"]
RULE_IDS = ["empty_text", "missing_source", "stale", "run_status"]
ALLOWED = ("id", "text", "source", "as_of", "tags")


class Fail(Exception):
    pass


def check(cond, msg):
    if not cond:
        raise Fail(msg)


def read_text(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def import_module(name):
    sys.path.insert(0, HERE)
    try:
        return __import__(name)
    except Exception as e:
        raise Fail("cannot import %s: %s" % (name, e))


def split_labels(cell):
    return sorted([p.strip() for p in cell.split(";") if p.strip()])


def record_from_row(row):
    """Build the record dict check.lint expects from one data.csv row.

    check.lint's `fields` rule fires when the KEY SET differs from the five
    allowed keys. So an empty cell must mean an ABSENT key, not an empty
    string: L006/L015 have no as_of and L018 has no source, and those are
    exactly the rows whose computed labels carry `fields` alongside the
    key‑specific label. Emitting every key unconditionally (the previous
    behaviour) made `fields` fire on the wrong rows.
    """
    rec = {}
    for key in ALLOWED:
        val = row.get(key, "")
        if key == "tags":
            # Include tags key always, even if empty, to avoid the `fields`
            # rule firing for rows that have all other keys but an empty
            # tags column.
            if val.strip():
                rec[key] = val.split()
            else:
                rec[key] = []
            continue
        if val.strip():
            rec[key] = val
    return rec


def run_column_check():
    tool = import_module("add_disputed_column")
    check(hasattr(tool, "add_disputed"), "add_disputed_column has no add_disputed()")
    with open(DATA, encoding="utf-8", newline="") as fh:
        base_header = list(csv.DictReader(fh).fieldnames)
    with open(DATA, encoding="utf-8", newline="") as fh:
        out_text = tool.add_disputed(fh)
    rows = list(csv.DictReader(io.StringIO(out_text)))
    check(len(rows) == 20, "expected 20 rows out, found %d" % len(rows))
    header = list(rows[0].keys())
    check(header[-1] == "disputed", "last column is %r" % header[-1])
    check(header[:-1] == base_header, "original header changed: %r" % header[:-1])
    marked = [r["id"] for r in rows if r["disputed"] == "1"]
    check(marked == DISPUTED, "disputed ids %r, expected %r" % (marked, DISPUTED))
    check(sum(1 for r in rows if r["disputed"] == "0") == 17, "expected 17 zeros")
    return {"rows": len(rows), "disputed": marked}


def run_rules_check():
    rules = json.loads(read_text(RULES))
    check(isinstance(rules, list), "rules.json is not a list")
    by_id = {}
    for obj in rules:
        rid = obj.get("id")
        check(isinstance(rid, str) and rid.strip(), "rule without id: %r" % (obj,))
        check(rid in RULE_IDS, "unexpected rule id %r" % rid)
        check(rid not in by_id, "duplicate rule id %r" % rid)
        check(isinstance(obj.get("disputed_ids"), list),
              "rule %r lacks disputed_ids list" % rid)
        for did in obj["disputed_ids"]:
            check(did in DISPUTED, "rule %r claims undisputed %r" % (rid, did))
        by_id[rid] = obj
    for rid in RULE_IDS:
        check(rid in by_id, "rules.json has no object for %r" % rid)
    for rid in ("empty_text", "missing_source", "stale"):
        pred = by_id[rid].get("predicate", "")
        check(pred.strip().endswith("."), "rule %r predicate not a sentence" % rid)
        check(pred.count(".") == 1, "rule %r predicate > one sentence" % rid)
    check(by_id["run_status"].get("disputed_ids") == [], "run_status disputed_ids")
    check(by_id["run_status"].get("status") == "VERIFIED", "run_status.status not VERIFIED")
    return {"rules": sorted(by_id)}


def run_readme_check():
    text = read_text(README)
    low = text.lower()
    req = ["self-agreement is not accuracy", "dispute a label", "check.py: 17/20 agree"]
    for phrase in req:
        check(phrase in low, "README is missing the phrase %r" % phrase)
    for unwanted in ("unrun", "not run", "no run happened"):
        check(unwanted not in low, "README contains forbidden phrase %r" % unwanted)
    for rid in DISPUTED:
        check(rid in text, "README does not name %s as disputed" % rid)
    return {"readme": "all checks pass"}


def run_lint_check():
    # Run check.lint on every row of data.csv, compare with expected_labels.
    checker = import_module("check")
    agree = 0
    mismatches = []
    with open(DATA, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    check(len(rows) == 20, "expected 20 rows, found %d" % len(rows))
    for r in rows:
        rec = record_from_row(r)
        got = checker.lint(rec)
        exp = split_labels(r["expected_labels"])
        if got == exp:
            agree += 1
        else:
            mismatches.append(r["id"])
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
          % (col["rows"], ",".join(col["disputed"])) )
    print("PASS rules.json: ids %s; run_status %s"
          % (",".join(rules["rules"]), "VERIFIED"))
    print("PASS README: %s" % card["readme"])  # fixed syntax
    print("PASS check.lint: agreement %d/20, mismatches %s"
          % (lint["agree"], ",".join(lint["mismatches"])) )
    print("All self-tests passed. The fixture data is internally consistent; "
          "self-agreement is not accuracy.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
