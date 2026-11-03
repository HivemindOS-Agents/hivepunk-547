#!/usr/bin/env python3
# Self-test for the capture tool.
# Run with NO arguments, from this directory. No network; writes only to a
# temp dir. It imports capture.run_capture, builds two tiny fixture folders,
# runs the tool on each and compares what comes out with what should.
# Exits 0 only if every check passes. It fails if a capture is empty or if
# the tool only echoes a result instead of running anything.

import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def die(msg):
    sys.stderr.write("FAIL: %s\n" % msg)
    sys.exit(1)


GOOD = '''
import json, os, sys
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

FIXTURES = [
    '{"id": "L004", "disagree": true, "note": "hand empty_text; check computes empty_text; empty_text branch"}\n',
    '{"id": "L018", "disagree": false, "note": ""}\n',
]

BAD_FIXTURES = [
    '{"id": "L004", "disagree": true, "note": ""}\n',
    '{"id": "L018", "disagree": false, "note": ""}\n',
]


def build(script, records):
    d = tempfile.mkdtemp(prefix="captest-")
    with open(os.path.join(d, "self_test.py"), "w", encoding="utf-8") as fh:
        fh.write(script)
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
        if "PASS note rule: 2 records" not in r["stdout"]:
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
