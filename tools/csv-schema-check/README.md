# csv-schema-check

opportunity: none

A small read-only Python checker for a dataset CSV. It validates
that the CSV has the expected columns, that a source URL is
present and well-formed in every row, and that no required field
is empty. It prints the row count and a PASS/FAIL summary, and
writes nothing.

Live Hugging Face pages were not checked by this tool: it does
not use the network, does not fetch any URL, and does not verify
that a source URL is reachable or that its content matches the
row. It only checks that the URL string is well-formed.

## Files

- csv_schema_check.py
- README.md
- self_test.py

## How to run

From this folder:

~~~bash
# Check with the default schema (tool_name,description,detail,source):
python3 csv_schema_check.py /path/to/data.csv

# Custom expected columns and required fields:
python3 csv_schema_check.py /path/to/data.csv --columns name,description,source --required name,source --url-column source

# Check several files at once:
python3 csv_schema_check.py a.csv b.csv

# Self-test (no arguments, no network, temp files only):
python3 self_test.py
~~~

On success it prints e.g. `PASS: data.csv (3 rows, columns:
tool_name,description,detail,source)` and exits 0. Otherwise it
prints one `FAIL:` line per specific problem plus a summary line
and exits 1, e.g.:

~~~text
FAIL: data.csv: missing expected column 'detail' (header: tool_name,description,source)
FAIL: data.csv: row 2: required field 'description' is empty
FAIL: data.csv: row 3: source URL in 'source' is not a well-formed http/https URL: 'not a url'
FAIL: data.csv (3 rows)
~~~

Options: `--columns a,b,c` sets the expected columns (default
`tool_name,description,detail,source`); `--required a,b` sets
the required fields (default: all expected columns); `--url-column
source` names the column that must hold a URL in every row
(default: `source`). Extra columns in the header are allowed and
reported as a NOTE. A well-formed URL needs an http/https scheme,
a non-empty host (dotted or `localhost`), no spaces or invalid
characters, and a valid port if given.

It only reads the named CSV file, writes nothing, uses no network,
and publishes nothing.

## Untested

- Untested against live Hugging Face datasets or pages: no live
  dataset CSV was read by this tool, and source-URL reachability
  and content accuracy were not checked (see above).
- Only the default schema (tool_name,description,detail,source)
  matches the earlier agent-memory dataset shape; other dataset
  shapes need `--columns`/`--required` and were not tested live.
- Malformed CSV quoting, very large files, duplicate header
  names, and non-UTF-8 encodings beyond a UTF-8 BOM were not
  tested; such files report a read error rather than a schema
  result.
- `SELFTEST_OUTPUT.md` in this folder, if present later, is
  written by the HivemindOS runner after the commit; this tool
  never writes it, and no output or pass line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
