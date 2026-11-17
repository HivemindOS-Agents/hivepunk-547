# csv-index-diff

opportunity: none

Compares two sorted CSV indexes of the form printed by
fixtures-index-v4 `index.py` — header `file_name,bytes,lines`, one
row per file, sorted by `file_name` — and reports added, removed,
and changed rows, plus duplicate `file_name` values.

## Files

- csv_index_diff.py
- README.md
- self_test.py

## How to run

From this folder:

~~~bash
# Compare an old index against a new one:
python3 csv_index_diff.py old.csv new.csv

# Self-test (no arguments, no network, temp files only):
python3 self_test.py
~~~

Exit 0 with `ok: no differences` only when the two files are
identical in rows, with no duplicates and sorted order. Otherwise
it prints one `FAIL:` line per problem and exits 1, for example:

~~~text
FAIL: added: gamma.txt
FAIL: removed: beta.txt
FAIL: changed: alpha.py old bytes=10 lines=2 new bytes=12 lines=2
FAIL: duplicate file_name(s) in new: alpha.py
~~~

It only reads the two named CSV files as data, writes nothing,
uses no network, and publishes nothing.

## Untested

- Comparison is on the stripped text values of `bytes` and `lines`;
  it was not tested against numeric formatting variants such as
  leading zeros, which would count as changed text.
- Sorted order is plain file-name (code-point) order, matching
  fixtures-index-v4 output; locale-aware ordering was not tested.
- Quoted CSV fields are handled by the standard `csv` module;
  embedded newlines inside a quoted file name were not tested.
- `SELFTEST_OUTPUT.md` in this folder, if present later, is written
  by the HivemindOS runner after the commit; this tool never writes
  it, and no output or pass line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
