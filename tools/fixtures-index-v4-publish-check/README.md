# fixtures-index-v4-publish-check

A pre-publish check for the fixtures-index-v4 dataset package: it validates
`data.csv` from `tools/fixtures-index-v4-dataset-package` before it is
published, using a local copy of that `data.csv` in this folder so the
check runs alone.

## What it checks

- Exactly 4 data rows, with 4 unique `file_name` values (no duplicates).
- The header has exactly the required columns: `file_name`, `source_url`,
  `description` — no missing column, no extra column.
- Every `file_name`, `source_url` and `description` is non-empty.
- Every `source_url` is under `tools/fixtures-index-v4`: it contains the
  path segment `tools/fixtures-index-v4/` and ends with `/` plus that
  row's `file_name`.

`check_package.py` only reads the CSV as data; it runs no code it reads,
writes nothing, and publishes nothing.

## How to run

From this folder:

~~~bash
# Check the included data.csv (exit 0 ok, exit 1 with FAIL lines):
python3 check_package.py

# Check a different CSV:
python3 check_package.py /path/to/data.csv

# Self-test (no arguments, no network):
python3 self_test.py
~~~

## Untested

- The `source_url` values were not fetched or checked against live GitHub
  in this step: the check is string-only (path segment plus file_name tail),
  so a URL with the right shape but a dead link still passes.
- The `data.csv` copy here was not compared byte-for-byte against the live
  `tools/fixtures-index-v4-dataset-package/data.csv` in this step; it was
  carried from that package's records as listed in `tools`. Re-sync it if
  the dataset package is rebuilt.
- Only the exact header set is accepted; a CSV that adds a useful extra
  column fails by design and would need the required-column list changed
  in `check_package.py`.
- `SELFTEST_OUTPUT.md` in this folder, if present later, is written by the
  HivemindOS runner after the commit; this tool never writes it, and no
  output or pass line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
