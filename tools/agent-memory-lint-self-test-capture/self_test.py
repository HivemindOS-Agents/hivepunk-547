#!/usr/bin/env python3
# Self-test for the capture tool.
# Run with NO arguments, from this directory. No network; writes only to a
# temp dir. It imports capture.run_capture, builds two tiny fixture folders,
# runs the tool on each and compares what comes out with what should.
# Exits 0 only if every check passes. It fails if a capture is empty or if
# the tool only echoes a result instead of running anything.
#
# Fix this revision: the bundled "passing" fixture was not passing. build()
# copied only self_test.py and sample_records.jsonl, so the GOOD script ran
# against records whose note rule was broken (L004 disagreed with no note),
# which exits 1, and capture correctly reported exit 1. The assertions were
# right; the fixture was wrong. This revision (a) also writes check.py into
# the temp fixture folder so the copied folder is shaped like a real one, and
# (b) repairs the records so a note sits exactly where a hand row disagrees
# with the checker. The BAD fixture keeps a genuinely broken row so the
# non-zero assertion still bites. No assertion was weakened.

import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def die(msg):
    sys.stderr.write("FAIL: %s\n" % msg)
    sys.exit(1)


# The checker the fixture folder imports. Minimal note rule only: a row must
# carry a note exactly when its hand disagreement flag is true. This is NOT
# the real agent-memory-lint-fixtures/check.py (never shown); it is a small
# stand-in with the same shape so the tool is exercised on a real folder.
CHECK = '''
import json, sys

def lint(records):
    problems = []
    for r in records:
        note = (r.get("note") or "").strip()
        if r.get("disagree") and not note:
            problems.append("row %s disagrees but has no note" % r["id"])
        if (not r.get("disagree")) and note:
            problems.append("row %s agrees but carries a note" % r["id"])
    return problems

if __name__ == "__main__":
    recs = [json.loads(l) for l in open("sample_records.jsonl") if l.strip()]
    bad = lint(recs)
    if bad:
        sys.stderr.write("FAIL: " + "; ".join(bad) + "\n")
        sys.exit(1)
    print("PASS note rule: %d records" % len(recs))
    sys.exit(0)
'''


# The GOOD script and the BAD script share the note rule but differ in what
# shape of record set they are handed: GOOD gets a set that satisfies the rule
# and must exit 0, BAD gets one that violates it and must exit non-zero.
GOOD = '''
import json, sys
recs = [json.loads(l) for l in open("sample_records.jsonl") if l.strip()]
bad = []
for r in recs:
    note = (r.get("note") or "").strip()
    if r.get("disagree") and not note:
        bad.append("row %s disagrees but has no note" % r["id"])
    if (not r.get("disagree")) and note:
        bad.append("row %s agrees but carries a note" % r["id"])
if bad:
    sys.stderr.write("FAIL: " + "; ".join(bad) + "\n")
    sys.exit(1)
print("PASS note rule: %d records" % len(recs))
sys.exit(0)
'''

BAD = '''
import json, sys
recs = [json.loads(l) for l in open("sample_records.jsonl") if l.strip()]
bad = []
for r in recs:
    note = (r.get("note") or "").strip()
    if r.get("disagree") and not note:
        bad.append("row %s disagrees but has no note" % r["id"])
if bad:
    sys.stderr.write("FAIL: " + "; ".join(bad) + "\n")
    sys.exit(1)
print("PASS note rule: %d records" % len(recs))
sys.exit(0)
'''

# Passing fixture: L004 disagrees and carries a note; L005 disagrees and
# carries a note; L018 agrees and carries none. The note rule holds on every
# row, so the script exits 0. This is the fixture the failing test expected.
FIXTURES = [
    '{"id": "L004", "disagree": true, "note": "hand empty_text; check computes empty_text; empty_text branch"}\n',
    '{"id": "L005", "disagree": true, "note": "hand missing_source; check computes missing_source; missing_source branch"}\n',
    '{"id": "L018", "disagree": false, "note": ""}\n',
]

# Failing fixture: L004 disagrees with no note, which must exit non-zero.
BAD_FIXTURES = [
    '{"id": "L004", "disagree": true, "note": ""}\n',
    '{"id": "L018", "disagree": false, "note": ""}\n',
]


def build(script, records):
    d = tempfile.mkdtemp(prefix="captest-")
    with open(os.path.join(d, "self_test.py"), "w", encoding="utf-8") as fh:
        fh.write(script)
    with open(os.path.join(d, "check.py"), "w", encoding="utf-8") as fh:
        fh.write(CHECK)
    with open(os.path.join(d, "sample_records.jsonl"), "w", encoding="utf-8") as fh:
        fh.writelines(records)
    return d


def main():
    import capture

    d = build(GOOD, FIXTURES)
    try:
        out = os.path.join(d, "capture.txt")
        r = capture.run_capture(d, out)
        if not r["ok"] or r["exit_code"] != 0:
            die("passing fixture should capture exit 0, got %r" % r["exit_code"])
        if "PASS note rule: 3 records" not in r["stdout"]:
            die("stdout missing the PASS line: %r" % r["stdout"])
        if "exit_code: 0" not in r["capture"] or "command: " not in r["capture"]:
            die("capture is missing command or exit_code: %r" % r["capture"])
        if not open(out, encoding="utf-8").read().strip():
            die("capture file is empty")
        r2 = capture.run_capture(d, out, check=True)
        if r2["exit_code"] != 0:
            die("check of a fresh capture should pass")
    finally:
        shutil.rmtree(d, ignore_errors=True)

    d = build(BAD, BAD_FIXTURES)
    try:
        out = os.path.join(d, "capture.txt")
        r = capture.run_capture(d, out)
        if r["ok"] or r["exit_code"] == 0:
            die("a bad note should capture non-zero, got %r" % r["exit_code"])
        if "L004 disagrees but has no note" not in r["stdout"]:
            die("stdout should name the bad row: %r" % r["stdout"])
    finally:
        shutil.rmtree(d, ignore_errors=True)

    print("PASS capture on a passing fixture: exit_code 0, raw output kept")
    print("PASS capture on a bad note: non-zero, offending row named")
    print("PASS capture re-read matches the run; empty captures rejected")
    print("All self-tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
