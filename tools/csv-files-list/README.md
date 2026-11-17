# csv-files-list

A small tool that reads the `file_name` column of a `data.csv` and prints
a Markdown Files list in the format the card-check tool
(`tools/fixtures-index-v4-card-check/card_check.py`) parses: a `## Files`
heading followed by one `- name` bullet per `file_name`, in CSV order.

## How to run

From this folder:

~~~bash
# Print the Files list for the included data.csv:
python3 csv_files.py

# Print it for another CSV:
python3 csv_files.py /path/to/data.csv

# Self-test (no arguments, no network, local sample CSVs only):
python3 self_test.py
~~~

Example output for the included `data.csv`:

~~~text
## Files

- inventory.py
- self_test.py
- README.md
- INVENTORY.md
~~~

It skips fully blank rows and uses the standard `csv` module, so quoted
names are read as written (for example a quoted name containing a comma
such as `"data,set.csv"` stays one name). It exits 1 with `FAIL:` lines
for a missing file, a missing `file_name` column, an empty `file_name`
in a non-blank row, duplicate names, or no values at all. It only reads
the input file as data, writes nothing, uses no network, and publishes
nothing.

## Untested

- Only the `file_name` column is read; other columns, frontmatter, the
  dataset name, and whether the listed files exist are not checked here.
- A `file_name` containing whitespace or a backtick is printed verbatim,
  but the card-check bullet parser does not accept whitespace or backticks
  inside a bullet name, so such names would need a different list format
  and were not tested against a live card.
- Duplicate detection is exact after stripping surrounding whitespace;
  case-only differences are treated as different names.
- `SELFTEST_OUTPUT.md` in this folder, if present later, is written by
  the HivemindOS runner after the commit; this tool never writes it,
  and no output or pass line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
