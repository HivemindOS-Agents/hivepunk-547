# fixtures-index-v4-publish-check

A pre-publish check for the fixtures-index-v4 files inventory: it verifies
that the included `inventory.csv` is exactly the 4-row inventory it claims
to be, before anyone publishes it as a dataset.

## What it checks

- Exactly 4 data rows, with 4 unique `file_name` values (no duplicates).
- The header has exactly the required columns: `file_name`, `source_url`,
  `description` — no missing column, no extra column.
- Every `file_name`, `source_url` and `description` is non-empty.
- Every `source_url` is under `tools/fixtures-index-v4`: it contains the
  path segment `tools/fixtures-index-v4/` and ends with `/` plus that
  row's `file_name`.

`inventory.csv` in this folder is the inventory of the four files of the
`fixtures-index-v4` tool (`inventory.py`, `self_test.py`, `README.md`,
`INVENTORY.md`), carried from the earlier fixtures-index-v4-files-inventory
tool. `verify_inventory.py` only reads the CSV as data; it runs no code it
reads, writes nothing, and publishes nothing.

## How to run

From this folder:

~~~bash
# Check the included inventory.csv (exit 0 ok, exit 1 with FAIL lines):
python3 verify_inventory.py

# Check a different CSV:
python3 verify_inventory.py /path/to/inventory.csv

# Self-test (no arguments, no network):
python3 self_test.py
~~~

## Untested

- The `source_url` values were not fetched or checked against live GitHub
  in this step: the check is string-only (path segment plus file_name tail),
  so a URL with the right shape but a dead link still passes.
- Only the exact header set is accepted; a CSV that adds a useful extra
  column (for example a `hash` column) fails by design and would need the
  required-column list changed in `verify_inventory.py`.
- The four file names come from the earlier inventory tool's records as
  carried in `tools`, not from a fresh listing of live
  `tools/fixtures-index-v4`; if that folder gains or loses a file, both
  `inventory.csv` here and the expected count of 4 need updating.
- The docstrings were not executed by their author in this step (no shell);
  only the HivemindOS runner's self-test result confirms the exit code.
- `SELFTEST_OUTPUT.md` in this folder, if present later, is written by the
  HivemindOS runner after the commit; this tool never writes it, and no
  output or pass line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
