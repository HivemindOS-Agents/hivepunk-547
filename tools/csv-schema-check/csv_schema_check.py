#!/usr/bin/env python3
"""csv_schema_check.py: validate a dataset CSV's schema.

Usage (from this folder):
    python3 csv_schema_check.py data.csv
    python3 csv_schema_check.py data.csv --columns tool_name,description,detail,source
    python3 csv_schema_check.py data.csv --required tool_name,source --url-column source
    python3 csv_schema_check.py a.csv b.csv

Defaults: expected columns are tool_name,description,detail,source;
the URL column is "source"; every expected column is required.

Checks (read-only, no network, writes nothing):
  * the file exists, is UTF-8 CSV, and has a header row;
  * every expected column is present in the header (extra columns
    are allowed and reported as a note);
  * no required field is empty or whitespace-only in any row;
  * the URL column holds a well-formed http/https URL in every row.

Prints the row count and a PASS/FAIL summary. On success prints
"PASS: <file> (N rows, columns: ...)" and exits 0. Otherwise
prints one "FAIL: <file>: <problem>" line per problem and exits 1.
"""

import csv
import os
import sys
import urllib.parse

DEFAULT_COLUMNS = ["tool_name", "description", "detail", "source"]
INVALID_URL_CHARS = set(' <>"\'{}|^`')


def _is_url(value):
    if not value or any(c in INVALID_URL_CHARS for c in value):
        return False
    try:
        parts = urllib.parse.urlparse(value)
    except ValueError:
        return False
    if parts.scheme not in ("http", "https") or not parts.netloc:
        return False
    host = parts.hostname
    if not host:
        return False
    if host != "localhost" and "." not in host:
        return False
    try:
        port = parts.port
    except ValueError:
        return False
    if port is not None and not (1 <= port <= 65535):
        return False
    return True


def _parse_list(text):
    return [item.strip() for item in text.split(",") if item.strip()]


def check_file(path, expected_columns=None, url_column="source", required_columns=None):
    """Return (ok, problems, row_count, notes)."""
    expected = list(expected_columns) if expected_columns else list(DEFAULT_COLUMNS)
    required = list(required_columns) if required_columns is not None else list(expected)
    problems = []
    notes = []
    if not os.path.exists(path):
        return False, ["not found: %s" % path], 0, notes
    if not os.path.isfile(path):
        return False, ["not a file: %s" % path], 0, notes
    try:
        with open(path, encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            header = reader.fieldnames
            rows = list(reader)
    except (OSError, UnicodeError) as e:
        return False, ["could not read %s: %s: %s" % (path, type(e).__name__, e)], 0, notes
    except csv.Error as e:
        return False, ["invalid CSV in %s: %s" % (path, e)], 0, notes
    if not header or all(not (h or "").strip() for h in header):
        return False, ["%s: no header row found" % path], 0, notes
    header = [(h or "").strip() for h in header]
    row_count = len(rows)
    for col in expected:
        if col not in header:
            problems.append("%s: missing expected column '%s' (header: %s)" % (path, col, ",".join(header)))
    extra = [h for h in header if h and h not in expected]
    if extra:
        notes.append("extra column(s) allowed: %s" % ",".join(extra))
    if row_count == 0:
        problems.append("%s: no data rows (header only)" % path)
    for col in required:
        if col not in header:
            continue
        for i, row in enumerate(rows, 1):
            value = (row.get(col) or "").strip()
            if not value:
                problems.append("%s: row %d: required field '%s' is empty" % (path, i, col))
    if url_column and url_column in header:
        for i, row in enumerate(rows, 1):
            value = (row.get(url_column) or "").strip()
            if value and not _is_url(value):
                problems.append("%s: row %d: source URL in '%s' is not a well-formed http/https URL: %r" % (path, i, url_column, value))
    return not problems, problems, row_count, notes


def main(argv):
    args = list(argv[1:])
    columns = list(DEFAULT_COLUMNS)
    required = None
    url_column = "source"
    files = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--columns" and i + 1 < len(args):
            columns = _parse_list(args[i + 1]); i += 2
        elif arg.startswith("--columns="):
            columns = _parse_list(arg.split("=", 1)[1]); i += 1
        elif arg == "--required" and i + 1 < len(args):
            required = _parse_list(args[i + 1]); i += 2
        elif arg.startswith("--required="):
            required = _parse_list(arg.split("=", 1)[1]); i += 1
        elif arg == "--url-column" and i + 1 < len(args):
            url_column = args[i + 1]; i += 2
        elif arg.startswith("--url-column="):
            url_column = arg.split("=", 1)[1]; i += 1
        elif arg in ("-h", "--help"):
            print(__doc__.strip()); return 0
        elif arg.startswith("--"):
            print("FAIL: unknown option %s" % arg); return 1
        else:
            files.append(arg); i += 1
    if not files:
        print("FAIL: usage: python3 csv_schema_check.py FILE.csv [--columns a,b,c] [--required a,b] [--url-column source]")
        return 1
    if not columns:
        print("FAIL: --columns must name at least one column")
        return 1
    ok_all = True
    for path in files:
        ok, problems, row_count, notes = check_file(path, columns, url_column, required)
        if ok:
            print("PASS: %s (%d rows, columns: %s)" % (path, row_count, ",".join(columns)))
        else:
            ok_all = False
            for note in notes:
                print("NOTE: %s: %s" % (path, note))
            for p in problems:
                print("FAIL: " + p)
            print("FAIL: %s (%d rows)" % (path, row_count))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
