#!/usr/bin/env python3
# Top-level self-test for tools/agent-memory-lint-fixtures.
# Run with NO arguments, from this folder. No network, no writes.
#
# It imports the tool's own code (add_disputed_column.add_disputed and
# check.py's lint), runs both on the data actually bundled in this folder,
# and compares what comes out with what should. It also loads rules.json and
# asserts the rule table is complete and covers all three disputed ids.
# Exits 0 only when every check passes.
#
# NOTE: an earlier revision read sample_data.csv, which was never committed
# into this folder; that is why the previous run failed. This revision reads
# the committed data.csv instead. The transform was never wrong.

import csv
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data.csv")
RECORDS = os.path.join(HERE, "sample_records.jsonl")
RULES = os.path.join(HERE, "rules.json")
README = os.path.join(HERE, "README.md")
DISPUTED = ["L006", "L015", "L018"]
EXPECTED_AGREE = 17
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
    """Run the tool's own add_disputed() on the bundled data.csv."""
    tool = import_module("add_disputed_column")
    check(hasattr(tool, "add_disputed"), "add_disputed_column has no add_disputed()")

    with open(DATA, encoding="utf-8", newline="") as fh:
        base_header = list(csv.DictReader(fh).fieldnames)
    with open(DATA, encoding="utf-8", newline="") as fh:
        out_text = tool.add_disputed(fh)

    rows = list(csv.DictReader(io.StringIO(out_text)))
    check(len(rows) == 20, "expected 20 rows out, found %d" % len(rows))
    header = list(rows[0].keys())
    check(header[-1] == "disputed", "last column is %r, expected 'disputed'" % header[-1])
    check(header.count("disputed") == 1, "disputed column appears more than once")
    check(header[:-1] == base_header, "original header was changed: %r" % header[:-1])

    ids = [r["id"] for r in rows]
    check(ids == ["L%03d" % n for n in range(1, 21)], "ids are %r" % ids)
    check(set(r["disputed"] for r in rows) == {"0", "1"},
          "disputed holds values other than 0/1")
    marked = [r["id"] for r in rows if r["disputed"] == "1"]
    check(marked == DISPUTED,
          "disputed ids are %r, expected %r" % (marked, DISPUTED))
    zero = sum(1 for r in rows if r["disputed"] == "0")
    check(zero == 17, "expected 17 rows with disputed=0, found %d" % zero)
    return {"rows": len(rows), "disputed": marked,
            "first": ids[0], "last": ids[-1]}


def run_lint_check():
    """Run check.py's own lint() on the bundled records and compare."""
    checker = import_module("check")
    check(hasattr(checker, "lint"), "check.py has no lint()")

    recs = []
    for line in read_text(RECORDS).splitlines():
        if line.strip():
            recs.append(json.loads(line))
    check(len(recs) == 20, "sample has %d records, expected 20" % len(recs))

    agree, mismatch, notes = 0, [], []
    for rec in recs:
        rec = dict(rec)
        rid = rec["id"]
        want = rec.pop("expected_labels")
        note = rec.pop("note", "").strip()
        got = checker.lint(rec)
        if got == want:
            agree += 1
            if note:
                notes.append("row %s agrees but carries a note" % rid)
        else:
            mismatch.append(rid)
            if not note:
                notes.append("row %s disagrees but has no note" % rid)
    check(not notes, "; ".join(notes))
    check(agree == EXPECTED_AGREE,
          "agreement is %d/20, expected %d/20" % (agree, EXPECTED_AGREE))
    check(mismatch == DISPUTED,
          "mismatches are %r, expected %r" % (mismatch, DISPUTED))
    return {"agree": agree, "mismatches": mismatch}


def run_rules_check():
    """rules.json: one object per rule id, predicates present, disputes covered."""
    rules = json.loads(read_text(RULES))
    check(isinstance(rules, list),
          "rules.json should be a list of rule objects, found %s" % type(rules).__name__)

    by_id = {}
    for obj in rules:
        check(isinstance(obj, dict), "a rule entry is not an object: %r" % (obj,))
        rid = obj.get("id")
        check(isinstance(rid, str) and rid.strip(),
              "a rule entry has no non-empty id: %r" % (obj,))
        check(rid in RULE_IDS, "unexpected rule id %r" % rid)
        check(rid not in by_id, "rule id %r appears more than once" % rid)
        by_id[rid] = obj

    for rid in RULE_IDS:
        check(rid in by_id, "rules.json has no object for rule %r" % rid)

    for rid in ("empty_text", "missing_source", "stale"):
        obj = by_id[rid]
        pred = obj.get("predicate")
        check(isinstance(pred, str) and pred.strip(),
              "rule %r has no non-empty predicate" % rid)
        check(pred.strip().endswith("."),
              "rule %r predicate is not a sentence ending in a period: %r" % (rid, pred))
        check(pred.count(".") == 1,
              "rule %r predicate is more than one sentence: %r" % (rid, pred))
        check(isinstance(obj.get("disputed_ids"), list),
              "rule %r has no disputed_ids list" % rid)
        for did in obj["disputed_ids"]:
            check(did in DISPUTED,
                  "rule %r claims undisputed id %r" % (rid, did))

    check(by_id["run_status"].get("predicate", "").strip(),
          "run_status has no non-empty predicate")
    check(by_id["run_status"].get("disputed_ids") == [],
          "run_status must carry an empty disputed_ids list")
    check(by_id["run_status"].get("status") == "UNRUN",
          "run_status.status must be exactly 'UNRUN', found %r"
          % by_id["run_status"].get("status"))

    covered = set()
    for rid in ("empty_text", "missing_source", "stale"):
        covered.update(by_id[rid]["disputed_ids"])
    missing = [d for d in DISPUTED if d not in covered]
    check(not missing,
          "disputed ids not covered by any rule: %r" % missing)
    return {"rules": sorted(by_id), "covered": sorted(covered)}


def run_readme_check():
    """The card must keep the caveat and name the three disputed ids."""
    text = read_text(README)
    low = text.lower()
    for phrase in ("unrun", "self-agreement is not accuracy",
                   "dispute a label"):
        check(phrase in low, "README is missing the phrase %r" % phrase)
    for rid in DISPUTED:
        check(rid in text, "README does not name %s as disputed" % rid)
    return {"readme": "caveats present"}


def main():
    try:
        col = run_column_check()
        lint = run_lint_check()
        rules = run_rules_check()
        card = run_readme_check()
    except Fail as e:
        sys.stderr.write("FAIL: %s\n" % e)
        return 1
    except Exception as e:  # noqa: BLE001
        sys.stderr.write("FAIL: unexpected %s: %s\n" % (type(e).__name__, e))
        return 1

    print("PASS add_disputed_column: %d rows, disputed=%s, first=%s, last=%s"
          % (col["rows"], ",".join(col["disputed"]), col["first"], col["last"]))
    print("PASS check.lint: agreement %d/20, mismatches %s"
          % (lint["agree"], ",".join(lint["mismatches"])))
    print("PASS rules.json: ids %s; disputes covered %s; run_status UNRUN"
          % (",".join(rules["rules"]), ",".join(rules["covered"])) )
    print("PASS README: %s" % card["readme"])
    print("All self-tests passed. No lint run is claimed; the captured run "
          "files remain UNRUN and the Viewer readback lines remain 'not yet read'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
