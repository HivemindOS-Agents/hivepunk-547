# package-list-check

opportunity: none

A small tool that validates a dataset-package folder: it compares the
regular files directly in the folder to the bullet list under
`## Files` (or `## File list`) in that folder's `README.md`, and
reports missing, extra, and duplicate entries with a nonzero exit.

## Files

- package_list_check.py
- README.md
- self_test.py

## How to run

From this folder:

~~~bash
# Check this folder against its own README Files list:
python3 package_list_check.py

# Check another package folder:
python3 package_list_check.py /path/to/package

# Self-test (no arguments, no network, local fixture folders only):
python3 self_test.py
~~~

On a match it prints `ok: ...` and exits 0. Otherwise it prints one
`FAIL:` line per problem and exits 1, for example:

~~~text
FAIL: file(s) on disk missing from Files list: data.csv
FAIL: file(s) listed but missing on disk: stray.py
FAIL: Files list duplicate(s): alpha.py
~~~

It only reads the target folder as data, writes nothing, uses no
network, and publishes nothing. Subdirectories are skipped: only
regular files directly in the folder count as the local file list,
and `README.md` itself must be listed if it is present.

## Untested

- Only files directly in the folder are compared; recursive
  (subdirectory) listings, hidden-file rules beyond skipping
  `__pycache__/` and `.git/`, and symlink targets were not tested
  against a live package tree.
- Bullet parsing matches the card-check format `- name` with no
  whitespace or backticks inside the name; a name containing
  whitespace or a backtick cannot be represented in that format and
  was not tested against a live card.
- Order of the list is not required to match disk order; only the
  sets and duplicates are compared. Duplicate detection is exact
  after stripping surrounding whitespace; case-only differences
  count as different names.
- `SELFTEST_OUTPUT.md` in this folder, if present later, is written
  by the HivemindOS runner after the commit; this tool never writes
  it, and no output or pass line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
