# card-files-sync

A small tool that checks a dataset card's Files list against its
`data.csv`: it compares the `file_name` column of `data.csv` to the
bullet list under `## Files` (or `## File list`) in `README.md`, and
exits nonzero listing missing, extra, and duplicate entries.

## Files

- sync_check.py
- README.md
- self_test.py
- data.csv

## How to run

From this folder:

~~~bash
# Check the included sample card and data.csv:
python3 sync_check.py

# Check other files:
python3 sync_check.py /path/to/README.md /path/to/data.csv

# Self-test (no arguments, no network, local fixtures only):
python3 self_test.py
~~~

On a match it prints `ok: ...` and exits 0. Otherwise it prints one
`FAIL:` line per problem and exits 1, for example:

~~~text
FAIL: file list missing from card: gamma.py
FAIL: file list has extra names not in data.csv: stray.py
FAIL: file list duplicate(s): alpha.py
~~~

It uses the standard `csv` module, so quoted names are read as written
(for example `"data,set.csv"` stays one name), and it skips fully
blank CSV rows. It only reads the two input files as data, writes
nothing, uses no network, and publishes nothing.

## Untested

- Only the `file_name` column and the Files list are compared;
  frontmatter, dataset name, other columns, and whether the listed
  files actually exist on disk are not checked here.
- Bullet parsing matches the card-check format `- name` with no
  whitespace or backticks inside the name; a name containing
  whitespace or a backtick cannot be represented in that format and
  was not tested against a live card.
- Order of the list is not required to match CSV order; only the
  sets and duplicates are compared.
- Duplicate detection is exact after stripping surrounding
  whitespace; case-only differences count as different names.
- `SELFTEST_OUTPUT.md` in this folder, if present later, is written
  by the HivemindOS runner after the commit; this tool never writes
  it, and no output or pass line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
