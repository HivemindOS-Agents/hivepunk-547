# duckophila-stated-facts: publish record

Status: publish package prepared in this folder. The live
Hub page was NOT fetched or confirmed in the step that
wrote this file, so every live entry below is an intended
value, not a confirmed one. The self-test result below IS
confirmed (runner output, see below).

## Intended live URL

https://huggingface.co/datasets/hivepunk-547-db38b7a4/duckophila-stated-facts

Account: hivepunk-547-db38b7a4 (owner account; no organisation).
Dataset name: duckophila-stated-facts

## Files to upload (from this folder only)

- facts.csv
- README_hf.md, uploaded as the dataset README (README.md)

Do not upload: build_facts.py, self_test.py, README.md,
ARTIFACTS.md, SELFTEST_OUTPUT.md.
Do not touch hivepunk-547-db38b7a4/agent-memory-lint-fixtures.

## Intended row count

facts.csv: 17 data rows plus 1 header row.
Columns: fact,source_url,label,note
Sources: only
https://github.com/first-it-consulting/duckophila and
https://github.com/joeynyc/awesome-microduck.

## Dataset card and licences

Card: README_hf.md. It states, per source:
- duckophila repo licence: UNKNOWN (licence file not read)
- awesome-microduck repo licence: UNKNOWN (licence file
  not read)
No licence text was invented for either source.

## Self-test output (confirmed)

Runner: HivemindOS bee-self-test, 2026-11-20 10:04 UTC
Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44716043935
Result: passed

~~~text
every built row has a non-empty http(s) source_url, a known label and a unique fact
all rows use only the two allowed sources, and both appear
facts.csv matches the built rows (17 rows)
every committed row has a non-empty source_url
validator rejects empty/off-scheme source_url, unknown label and duplicate fact
dataset card names both sources, states each licence as UNKNOWN and gives 17 rows
ARTIFACTS.md records intended URL, upload files, 17 rows, confirmed self-test run, marked live-unconfirmed
self-test: all checks passed
~~~

## Verification to do after publishing (not yet done)

The publish step should fetch and paste here:

1. The live dataset page URL (expected: the intended URL
   above) and confirm it loads under
   hivepunk-547-db38b7a4 as duckophila-stated-facts.
2. The live file list from the dataset tree page
   (expected: facts.csv and README.md, where README.md is
   the uploaded README_hf.md) - paste the actual list.
3. The live facts.csv row count (expected: 17 data rows
   plus header) - paste the actual count.
4. A fresh self-test run after any edit to this file.

Until those four are pasted, the live page, file list and
live row count remain NOT confirmed.

## Left for owner

Owner: run the HivemindOS publish step to publish the two
files above, then fetch the live Hub page and edit this
file to replace the intended URL, file list and row count
with the confirmed ones and paste the fresh self-test
output.
