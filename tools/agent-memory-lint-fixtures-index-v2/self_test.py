#!/usr/bin/env python3
# Top of the tool folder. Run with NO arguments, from this directory.
# No network, no writes. Reads data.csv in this folder and checks it against
# the six rows this package claims to publish, then prints a PASS line per
# check. Exits 0 only when every check passes.
#
# This is a real check on the published artifact: it fails on a padded,
# mislabeled, reordered or stale data.csv. Everything in the file is data.

import csv
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

    if c.failed:
        sys.stderr.write("self-test FAILED: %d check(s) failed\n" % c.failed)
        return 1
    sys.stdout.write("OK self-test passed: 6 rows, note rule verbatim, "
                     "one source URL, no checker run claimed.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
