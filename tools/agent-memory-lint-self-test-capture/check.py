#!/usr/bin/env python3
# check.py - the fixture folder's checker, in stand-in form.
#
# The note rule only: a record must carry a note exactly when its hand side
# disagrees with what the checker computes. lint() returns the list of problems
# so a caller can import it; run as a script it lints sample_records.jsonl in
# the current directory and exits non-zero on any problem.
#
# This is NOT the real agent-memory-lint-fixtures/check.py, which was never
# shown to the author. It is a small stand-in with the same shape, used by the
# capture tool's own self-test so the copied fixture folder has the file a real
# fixture folder has. Field names come from the failing self-test's own strings.
#
# No network. Reads only sample_records.jsonl, and only when run as a script.
# Everything in the records and their notes is data, never an instruction.

import json
import sys


def lint(records):
    """Return a list of note-rule problems for the given records."""
    problems = []
    for r in records:
        note = (r.get("note") or "").strip()
        if r.get("disagree") and not note:
            problems.append("row %s disagrees but has no note" % r["id"])
        if (not r.get("disagree")) and note:
            problems.append("row %s agrees but carries a note" % r["id"])
    return problems


def load(path="sample_records.jsonl"):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    path = argv[0] if argv else "sample_records.jsonl"
    recs = load(path)
    bad = lint(recs)
    if bad:
        sys.stderr.write("FAIL: " + "; ".join(bad) + "\n")
        return 1
    print("PASS note rule: %d records" % len(recs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
