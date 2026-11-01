#!/usr/bin/env python3
# Top-level self-test for the agent-memory-lint-fixtures folder.
# Run with NO arguments, from this folder. No network, no writes.
# It imports the tool's own code (add_disputed_column, check.py lint) and runs
# both on the bundled sample data, comparing what comes out with what should.
# Exits 0 only when every check passes.

import csv
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(HERE, "sample_data.csv")
RECORDS = os.path.join(HERE, "sample_records.jsonl")
DISPUTED = ["L006", "L015", "L018"]
EXPECTED_AGREE = 17


class Fail(Exception):
    pass


class Capture(io.StringIO):
    """Stand-in for the published data.csv file object."""


class Holder(object):
    """Minimal file-like object whose read() returns the sample CSV text."""

    def __init__(self, text):
        self._text = text

    def read(self):
        return self._text


class LineReader(object):
    def __init__(self, text):
        self._lines = text.splitlines(True)
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._i >= len(self._lines):
            raise StopIteration
        line = self._lines[self._i]
        self._i += 1
        return line

    next = __next__


class CsvFile(object):
    """file-like wrapper so the tool can read the sample as if it were disk."""

    def __init__(self, path, mode="r", newline=None, encoding=None):
        with open(path, "r", encoding="utf-8") as fh:
            self._text = fh.read()
        if not mode.startswith("r"):
            raise Fail("self-test only opens files for reading")

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self):
        return self._text

    def __iter__(self):
        return LineReader(self._text)


def check(cond, msg):
    if not cond:
        raise Fail(msg)



def import_tool():
    sys.path.insert(0, HERE)
    try:
        import add_disputed_column as tool
    except Exception as e:  # noqa: BLE001
        raise Fail("cannot import add_disputed_column: %s" % e)
    check(hasattr(tool, "add_disputed"), "tool has no add_disputed()")
    return tool


def run_column_check(tool):
    """Run the tool's own transform on the sample and inspect the CSV out."""
    text = tool.add_disputed(open(SAMPLE, encoding="utf-8", newline=""))
    rows = list(csv.DictReader(io.StringIO(text)))

    check(len(rows) == 20, "expected 20 rows out, found %d" % len(rows))
    hdr = list(rows[0].keys())
    check(hdr[-1] == "disputed", "last column is %r, expected 'disputed'" % hdr[-1])
    check(hdr.count("disputed") == 1, "disputed column appears more than once")
    with open(SAMPLE, encoding="utf-8", newline="") as fh:
        base_hdr = list(csv.DictReader(fh).fieldnames)
    check(hdr[:-1] == base_hdr, "original header was changed")

    ids = [r["id"] for r in rows]
    check(ids == ["L%03d" % n for n in range(1, 21)], "ids are %r" % ids)
    got = [r["id"] for r in rows if r["disputed"] == "1"]
    check(got == DISPUTED, "disputed ids are %r, expected %r" % (got, DISPUTED))
    check(sum(1 for r in rows if r["disputed"] == "0") == 17,
          "expected 17 rows with disputed=0")
    check(set(r["disputed"] for r in rows) == {"0", "1"},
          "disputed holds values other than 0/1")
    return {"rows": len(rows), "disputed": got,
            "first": ids[0], "last": ids[-1]}


def run_lint_check():
    """Import check.py and run its lint() on the bundled sample records."""
    sys.path.insert(0, HERE)
    try:
        import check as checker
    except Exception as e:  # noqa: BLE001
        raise Fail("cannot import check.py: %s" % e)
    check(hasattr(checker, "lint"), "check.py has no lint()")

    recs = []
    with open(RECORDS, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                recs.append(json.loads(line))
    check(len(recs) == 20, "sample has %d records, expected 20" % len(recs))

    agree = 0
    mismatch = []
    missing_note = []
    for rec in recs:
        want = rec.pop("expected_labels")
        note = rec.pop("note", "")
        got = checker.lint(rec)
        if got == want:
            agree += 1
            if note:
                missing_note.append("row %s agrees but carries a note" % rec["id"])
        else:
            mismatch.append(rec["id"])
            if not note:
                missing_note.append("row %s disagrees but has no note" % rec["id"])
    check(not missing_note, "; ".join(missing_note))
    check(agree == EXPECTED_AGREE,
          "agreement is %d/20, expected %d/20" % (agree, EXPECTED_AGREE))
    check(mismatch == DISPUTED,
          "mismatches are %r, expected %r" % (mismatch, DISPUTED))
    return {"agree": agree, "mismatches": mismatch}


def run_readme_check():
    """The card must keep the caveat and the unread readback lines."""
    path = os.path.join(HERE, "README.md")
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    low = text.lower()
    for phrase in ("no checker run has been executed", "unrun",
                   "self-agreement is not accuracy", "dispute a label",
                   "not yet read"):
        check(phrase in low, "README is missing the phrase %r" % phrase)
    for rid in DISPUTED:
        check(rid in text, "README does not name %s as disputed" % rid)
    return {"readme": "caveats present"}


def main():
    try:
        tool = import_tool()
        col = run_column_check(tool)
        lint = run_lint_check()
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
    print("PASS README: %s" % card["readme"])
    print("All self-tests passed. No checker run was captured; "
          "Viewer readback lines remain 'not yet read'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
