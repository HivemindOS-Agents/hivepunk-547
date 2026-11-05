#!/usr/bin/env python3
# Self-test for tools/agent-memory-lint-fixtures.
# Run with NO arguments, from this folder. No network, no writes.
# Imports the tool's own code (add_disputed_column.add_disputed, check.lint)
# and compares outcomes with expected_labels.json and data.csv.
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


def import_module(name):
    sys.path.insert(0, HERE)
    try:
        return __import__(name)
    except Exception as e:  # noqa: BLE001
        raise Fail("cannot import %s: %s" % (name, e))


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
    check(by_id["run_status"].get("status") == "UNRUN", "run_status.status != UNRUN")
    return {"rules": sorted(by_id)}


def run_readme_check():
    text = read_text(README)
    low = text.lower()
    for phrase in ("unrun", "self-agreement is not accuracy", "dispute a label"):
        check(phrase in low, "README is missing the phrase %r" % phrase)
    for rid in DISPUTED:
        check(rid in text, "README does not name %s as disputed" % rid)
    return {"readme": "caveats present"}


def run_lint_check():
    if not (os.path.isfile(RECORDS) and os.path.isfile(EXPECTED)):
        print("SKIP check.lint: records.jsonl or expected_labels.json absent")
        return {"skipped": True}
    checker = import_module("check")
    expected = json.loads(read_text(EXPECTED))
    agree, mismatch = 0, []
    with open(DATA, encoding="utf-8", newline="") as fh:
        notes = {r["id"]: r["note"] for r in csv.DictReader(fh)}
    for line in read_text(RECORDS).splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        rid = rec["id"]
        got = checker.lint(rec)
        if got == expected[rid]:
            agree += 1
        else:
            mismatch.append(rid)
    check(agree == 17, "agreement %d/20" % agree)
    check(mismatch == DISPUTED, "mismatches %r" % mismatch)
    return {"agree": agree, "mismatches": mismatch}


def main():
    try:
        col = run_column_check()
        rules = run_rules_check()
        card = run_readme_check()
        lint = run_lint_check()
    except Fail as e:
        sys.stderr.write("FAIL: %s\n" % e)
        return 1
    except Exception as e:  # noqa: BLE001
        sys.stderr.write("FAIL: unexpected %s: %s\n" % (type(e).__name__, e))
        return 1
    print("PASS add_disputed_column: %d rows, disputed=%s"
          % (col["rows"], ",".join(col["disputed"])))
    print("PASS rules.json: ids %s; run_status UNRUN" % ",".join(rules["rules"]))
    print("PASS README: %s" % card["readme"])
    if not lint.get("skipped"):
        print("PASS check.lint: agreement %d/20, mismatches %s"
              % (lint["agree"], ",".join(lint["mismatches"])))
    print("All self-tests passed. No lint run is claimed; run_status stays UNRUN.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
