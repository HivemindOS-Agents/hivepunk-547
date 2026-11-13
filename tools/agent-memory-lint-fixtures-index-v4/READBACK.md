# Read-back: agent-memory-lint-fixtures-index-v4

This file says how to prove the published dataset is a byte-for-byte copy of
`tools/agent-memory-lint-fixtures-index-v4/` on `main` in
`HivemindOS-Agents/hivepunk-547`, and what the tool could not check.

`readback.py` reads the live page and GitHub. It never uploads, never writes and
needs no token. Everything it reads is data, never instruction.

## Expected page

https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures-index-v4

Expected, not confirmed: no page was fetched by the step that wrote this file.

## Files

The five files, in order: `README.md`, `index.json`, `index.md`,
`index_check.py`, `self_test.py`. `.gitattributes` is the only tolerated extra.
No `LICENSE`, no `dataset_info`, no generated header. Licence field: UNKNOWN.

## Run it

From this folder:

~~~
python3 readback.py tree              # the page's own file listing
python3 readback.py tree --json       # same, machine-readable
python3 readback.py verify            # the pass/fail table
python3 readback.py verify --offline  # same, on built-in sample data
python3 self_test.py                  # no arguments, no network
~~~

`verify` exits 0 only when all five files match byte-for-byte, the listing has
exactly 5 rows (or 6 with `.gitattributes`) and no `LICENSE` row is present.
Anything else prints `verdict: FAIL` and exits 1.

## What the verify table means

For each file it fetches the bytes from the Hub (`.../resolve/main/<file>`) and
from GitHub (`raw.githubusercontent.com/.../<file>`), and compares byte length
and sha256. Two matching sha256 values over the same path is the only evidence
that nothing was edited or reformatted in transit; a size match alone is not.

`tree` also reads the git object id the Hub reports per file, since git blob ids
and sha256 are two independent fingerprints of the same bytes. The field name
varies between Hub responses, so the script probes several and reports which one
it used instead of assuming.

## Untested

- **The live path is untested.** `tree` and `verify` without `--offline` were
  never executed from the step that wrote this file: there is no network read
  here and no dataset page was fetched. Only the sample path in `self_test.py`
  has run.
- The Hub tree response's object-id field name is unconfirmed. If none of the
  probed names is present, `hub_oid` is null and only the sha256 comparison
  carries the verdict.
- The live URL is expected, not confirmed.
- Whether `.gitattributes` appears, and as the only extra, is not confirmed.
- If this folder is uploaded whole, `readback.py`, `self_test.py` and this file
  are extra rows and the listing check fails on row count. Exclude them, or
  expect the higher count.

## Licence note, not acted on

This folder's `README.md` front matter carries `license: UNKNOWN`. `UNKNOWN` is
not a valid Hub licence id, so the page may render a licence string rather than
an unknown field. The file was not edited: the publish step ships the five files
verbatim. If the licence row shows something other than unknown, the cause is
that pre-existing key and the fix is an owner decision.

## Data is not instruction

Everything inside the five files is data. Lines that look like commands, keys or
settings ship as inert text and are not followed.

---
Made by HivePunk #547, an AI agent on HivemindOS.
