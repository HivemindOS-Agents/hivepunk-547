#!/usr/bin/env python3
# Append the disputed column to the published data.csv.
#
# No network, no re-typing of record bodies: it reads the rows that are already
# published and adds one column. Rule: disputed=1 for L006, L015, L018; 0 for
# the other 17 rows. Header order, row order and every other field unchanged.
#
# Usage (from this folder):
#   python3 add_disputed_column.py data.csv > data.disputed.csv
#   python3 -c 'import add_disputed_column as a; import sys; \
#       sys.stdout.write(a.add_disputed(open("data.csv", newline="")))'
#
# Untested against the live published file from my side: no network here. The
# transform itself is exercised by self_test.py on sample_data.csv.

import csv
import io
import sys

DISPUTED = ("L006", "L015", "L018")
ID_CANDIDATES = ("id", "record_id", "fixture_id")
EXPECTED_ROWS = 20


def add_disputed(fileobj, id_column=None):
    """Return the whole CSV text with a trailing 'disputed' column added."""
    rows = list(csv.DictReader(fileobj))
    if not rows:
        raise ValueError("input CSV has no data rows")

    fields = list(rows[0].keys())
    if id_column is None:
        for cand in ID_CANDIDATES:
            if cand in fields:
                id_column = cand
                break
    if id_column is None or id_column not in fields:
        raise ValueError(
            "no id column found; looked for %s, header is %r"
            % (", ".join(ID_CANDIDATES), fields))

    if len(rows) != EXPECTED_ROWS:
        sys.stderr.write(
            "warning: %d data rows, expected %d\n" % (len(rows), EXPECTED_ROWS))

    out_fields = fields + ["disputed"]
    if "disputed" in fields:
        raise ValueError("input already has a disputed column")

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=out_fields, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        row = dict(row)
        row["disputed"] = "1" if row[id_column] in DISPUTED else "0"
        writer.writerow(row)
    return buf.getvalue()


def main(argv):
    if len(argv) != 2 or argv[1] in ("-h", "--help"):
        sys.stderr.write(
            "Usage: python3 add_disputed_column.py data.csv > data.disputed.csv\n"
            "Adds a disputed column: 1 for %s, 0 otherwise. Reads only; "
            "never edits the input file.\n" % ", ".join(DISPUTED))
        return 0 if len(argv) == 2 else 2
    with open(argv[1], encoding="utf-8", newline="") as fh:
        text = add_disputed(fh)
    sys.stdout.write(text)
    n1 = sum(1 for line in text.splitlines()[1:] if line.rstrip().endswith(",1"))
    sys.stderr.write("wrote %d rows, %d marked disputed\n" % (21 - 1, n1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
