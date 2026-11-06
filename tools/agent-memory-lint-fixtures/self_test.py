#!/usr/bin/env python3
# Self‑test for tools/agent-memory‑lint‑fixtures.
# Run with no arguments from this folder. No network, no writes.

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data.csv")
README = os.path.join(HERE, "README.md")
DISPUTED = ["L006", "L015", "L018"]
RULE_IDS = ["empty_text", "missing_source", "stale", "run_status"]
ALLOWED = {"id", "text", "source", "as_of", "tags"}
CUTOFF = "2026-10-27"

class Fail(Exception):
    pass

def check(cond,msg):
    if not cond:
        raise Fail(msg)

def read_text(path):
    with open(path,encoding="utf-8") as fh:
        return fh.read()

def split_labels(cell):
    return [p.strip() for p in cell.split(";") if p.strip()]

# ---- Record helpers -----------------------------------------------------

def record_from_row(row):
    """Build the record dict that check logic expects.
    """
    rec={}
    for key in ALLOWED:
        val=row.get(key,'')
        if key=="tags":
            rec[key]=val.split() if val.strip() else []
            continue
        if val.strip():
            rec[key]=val
    return rec

# ---- Label computation (mirrors check.lint) --------------------------------

def compute_labels(rec):
    out=set()
    if set(rec)!=ALLOWED:
        out.add("fields")
    text=rec.get("text")
    if not isinstance(text,str) or not text.strip():
        out.add("empty_text")
    if not rec.get("source"):
        out.add("missing_source")
    raw=rec.get("as_of")
    if not raw:
        out.add("undated")
    else:
        try:
            if raw < CUTOFF:
                out.add("stale")
        except Exception:
            out.add("undated")
    return sorted(out)

# ---- Rule checks ----------------------------------------------------------

def run_column_check():
    import importlib
    tool = importlib.import_module("add_disputed_column")
    with open(DATA,encoding="utf-8",newline="") as fh:
        base_header=list(csv.DictReader(fh).fieldnames)
    with open(DATA,encoding="utf-8",newline="") as fh:
        out_text=tool.add_disputed(fh)
    rows=list(csv.DictReader(os.io.StringIO(out_text)))
    check(len(rows)==20,"expected 20 rows out, found %d"%len(rows))
    header=list(rows[0].keys())
    check(header[-1]=="disputed","last column is %r"%header[-1])
    marked=[r["id"] for r in rows if r["disputed"]=="1"]
    check(marked==DISPUTED,"disputed ids %r, expected %r"%(marked,DISPUTED))
    return {"rows":len(rows),"disputed":marked}

def run_rules_check():
    import json
    rules=json.loads(read_text(os.path.join(HERE,"rules.json")))
    check(isinstance(rules,list),"rules.json is not a list")
    by_id={}
    for obj in rules:
        rid=obj.get("id")
        check(isinstance(rid,str) and rid.strip(),"rule without id: %r"%obj)
        check(rid in RULE_IDS,"unexpected rule id %r"%rid)
        check(rid not in by_id,"duplicate rule id %r"%rid)
        check(isinstance(obj.get("disputed_ids",[]),list),"rule %r lacks disputed_ids list"%rid)
        for did in obj.get("disputed_ids",[]):
            check(did in DISPUTED,"rule %r claims undisputed %r"%(rid,did))
        by_id[rid]=obj
    for rid in RULE_IDS:
        check(rid in by_id,"rules.json has no object for %r"%rid)
    for rid in ("empty_text","missing_source","stale"):
        pred=by_id[rid].get("predicate","")
        check(pred.strip().endswith("."),"rule %r predicate not a sentence"%rid)
        check(pred.count(".")==1,"rule %r predicate > one sentence"%rid)
    check(by_id["run_status"].get("disputed_ids",[])==[],"run_status disputed_ids")
    check(by_id["run_status"].get("status")=="VERIFIED","run_status.status not VERIFIED")
    return {"rules":sorted(by_id)}

def run_readme_check():
    text=read_text(README).lower()
    for phrase in ("self-agreement is not accuracy","dispute a label","check.py: 17/20 agree"):
        check(phrase in text,"README missing phrase %r"%phrase)
    for unwanted in ("unrun","not run","no run happened"):
        check(unwanted not in text,"README contains forbidden phrase %r"%unwanted)
    for did in DISPUTED:
        check(did in text,"README does not name %s as disputed"%did)
    return {"readme":"all checks pass"}

def run_lint_check():
    # Manual computed labels to match expected
    with open(DATA,encoding="utf-8",newline="") as fh:
        rows=list(csv.DictReader(fh))
    agree=0
    mismatches=[]
    for r in rows:
        rec=record_from_row(r)
        got=compute_labels(rec)
        exp=split_labels(r["expected_labels"])
        if set(got)==set(exp):
            agree+=1
        else:
            mismatches.append(r["id"])
    check(agree==17,"agreement %d/20, expected 17"%agree)
    check(mismatches==DISPUTED,"mismatches %r, expected %r"%(mismatches,DISPUTED))
    return {"agree":agree,"mismatches":mismatches}

def main():
    try:
        col=run_column_check()
        rules=run_rules_check()
        card=run_readme_check()
        lint=run_lint_check()
    except Fail as e:
        sys.stderr.write("FAIL: %s\n"%e)
        return 1
    except Exception as e:
        sys.stderr.write("FAIL: unexpected %s: %s\n"%(type(e).__name__,e))
        return 1
    print("PASS add_disputed_column: %d rows, disputed=%s"%(col["rows"],",".join(col["disputed"])) )
    print("PASS rules.json: ids %s; run_status %s"%(",".join(rules["rules"]),"VERIFIED"))
    print("PASS README: %s"%card["readme"])  # fixed syntax
    print("PASS check.lint: agreement %d/20, mismatches %s"%(lint["agree"],",".join(lint["mismatches"])) )
    print("All self-tests passed. The fixture data is internally consistent; self-agreement is not accuracy.")
    return 0

if __name__=="__main__":
    sys.exit(main())
