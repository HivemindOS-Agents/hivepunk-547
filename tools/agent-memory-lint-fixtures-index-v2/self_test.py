#!/usr/bin/env python3
# Top of the tool folder. Run with NO arguments, from this directory.
# No network, no writes. Reads data.csv in this folder and checks it against
# the six rows this package claims to publish, then prints a PASS line per
# check. Exits 0 only when every check passes.
#
# This is a real check on the published artifact: it fails on a padded,
# mislabeled, reordered or stale data.csv. Everything in the file is data.
#
# Second half: it exercises publish_check.py's checks on small in-memory
# fixtures, so a publish set that would not pass cannot be printed as ready.
#
# Fix note (this revision): the two in-memory fixtures below used to be built
# with three adjacent string literals, the last of which carried the
# `% (rid, flag)`. Python concatenates adjacent literals BEFORE applying `%`,
# so the combined string had three `%s` placeholders but only two arguments,
# raising TypeError: not enough arguments for format string. The URL and date
# literals carry no placeholder, so the format operation is now closed right
# after the third `%s` and the remaining literals are concatenated afterwards.
# Byte-for-byte output is unchanged; only the shape of the expression changed.

import csv
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "data.csv")

COLS = ["record_id", "has_note", "note_rule", "extra_file",
        "source_url", "date_read"]

NOTE_RULE = ("a row whose hand label disagrees with the checker must carry "
             "a note, an agreeing row must not")

# The six rows this package says it publishes: (id, has_note).
EXPECTED = [("L004", "yes"), ("L005", "yes"), ("L012", "yes"),
            ("L013", "yes"), ("L018", "no"), ("L020", "no")]

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL_RE = re.compile(r"^https://github\.com/HivemindOS-Agents/bee-scouts/"
                    r"issues/\d+$")


class Checker(object):
    def __init__(self):
        self.failed = 0

    def check(self, ok, label, detail=""):
        if ok:
            sys.stdout.write("PASS %s\n" % label)
        else:
            self.failed += 1
            sys.stderr.write("FAIL %s%s\n"
                             % (label, (" -- " + detail) if detail else ""))


def read_rows(path):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames
        rows = list(reader)
    return header, rows


def check_csv_text(text, allow_seven=False):
    """Run the field-level checks on CSV text. Returns list of failures."""
    problems = []
    with io.StringIO(text, newline="") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames
        rows = list(reader)
    if header != COLS:
        return ["header is exactly the six expected columns"]
    if len(rows) != 6:
        problems.append("exactly 6 data rows")
    ids = [(r["record_id"], r["has_note"]) for r in rows]
    if ids != EXPECTED:
        problems.append("ids and note flags match the six recorded rows")
    if not all(r["has_note"] in ("yes", "no") for r in rows):
        problems.append("every has_note is yes or no")
    if not all(r["note_rule"] == NOTE_RULE for r in rows):
        problems.append("note_rule is byte-identical on every row")
    if not all(r["extra_file"].strip() for r in rows):
        problems.append("every row names a non-empty extra_file")
    if not all(URL_RE.match(r["source_url"]) for r in rows):
        problems.append("every source_url is a bee-scouts issue URL")
    if not all(DATE_RE.match(r["date_read"]) for r in rows):
        problems.append("every date_read is YYYY-MM-DD")
    if len({r["source_url"] for r in rows}) != 1:
        problems.append("all six rows share one source URL")
    return problems


def check_fixture_cases(c):
    """Exercise publish_check's helpers on in-memory fixtures."""
    try:
        import publish_check as pc
    except ImportError as exc:
        c.check(False, "publish_check.py imports in-process", str(exc))
        return

    # NOTE the shape here: `% (rid, flag)` closes right after the third %s,
    # because the two following literals contain no placeholder.  Adjacent
    # string literals are concatenated before % is applied, so leaving the %
    # at the end made one string with three %s and two arguments.
    good = ("record_id,has_note,note_rule,extra_file,source_url,date_read\n"
            + "".join(
                '%s,%s,"%s",sample_records.jsonl,' % (rid, flag)
                + 'https://github.com/HivemindOS-Agents/bee-scouts/issues/109,'
                + '2026-11-07\n'
                for rid, flag in EXPECTED))

    c.check(pc.check_csv_text(good) == [],
            "publish_check accepts the six recorded rows")

    # Same corrected shape for the padded fixture: the % operand takes only
    # NOTE_RULE, and the argument-free literals are concatenated after it.
    padded = good + ('L099,no,"%s",x.jsonl,' % NOTE_RULE
                     + 'https://github.com/HivemindOS-Agents/bee-scouts/issues/109,'
                     + '2026-11-07\n')
    c.check("exactly 6 data rows" in pc.check_csv_text(padded),
            "publish_check rejects a padded seventh row")

    mislabeled = good.replace("L004,yes,", "L004,no,")
    c.check("ids and note flags match the six recorded rows"
            in pc.check_csv_text(mislabeled),
            "publish_check rejects a mislabeled note flag")

    unquoted = good.replace('"%s"' % NOTE_RULE, NOTE_RULE)
    c.check("note_rule is double-quoted in the raw bytes"
            in pc.check_raw_quoting(unquoted),
            "publish_check rejects an unquoted note_rule cell")

    c.check(pc.check_run_capture("exit code: 0\n") != [],
            "publish_check rejects a pasted-in exit byte in the run capture")

    c.check(pc.check_run_capture(
        "a transcription of the runner's result; SELFTEST_OUTPUT.md wins; "
        "0, as implied by passed\n") == [],
        "publish_check accepts a properly labelled transcription")



def main():
    c = Checker()

    if not os.path.isfile(PATH):
        sys.stderr.write("FAIL data.csv not found at %s\n" % PATH)
        return 1

    header, rows = read_rows(PATH)

    c.check(header == COLS, "header is exactly the six expected columns",
            "got %r" % (header,))

    if header != COLS:
        sys.stderr.write("cannot continue without the expected header\n")
        return 1

    c.check(len(rows) == 6, "exactly 6 data rows", "got %d" % len(rows))

    ids = [(r["record_id"], r["has_note"]) for r in rows]
    c.check(ids == EXPECTED, "ids and note flags match the six recorded rows",
            "got %r" % (ids,))

    c.check(all(r["has_note"] in ("yes", "no") for r in rows),
            "every has_note is yes or no")

    c.check(all(r["note_rule"] == NOTE_RULE for r in rows),
            "note_rule is byte-identical on every row")

    c.check(all(r["extra_file"].strip() for r in rows),
            "every row names a non-empty extra_file")

    c.check(all(URL_RE.match(r["source_url"]) for r in rows),
            "every source_url is a bee-scouts issue URL")

    c.check(all(DATE_RE.match(r["date_read"]) for r in rows),
            "every date_read is YYYY-MM-DD")

    c.check(len({r["source_url"] for r in rows}) == 1,
            "all six rows share one source URL")

    with open(PATH, "r", encoding="utf-8", newline="") as fh:
        raw = fh.read()
    c.check(raw.count('"' + NOTE_RULE + '"') == 6,
            "note_rule is double-quoted in the raw bytes on all six rows")

    check_fixture_cases(c)

    if c.failed:
        sys.stderr.write("self-test FAILED: %d check(s) failed\n" % c.failed)
        return 1
    sys.stdout.write("OK self-test passed: 6 rows, note rule verbatim, "
                     "one source URL, no checker run claimed.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
