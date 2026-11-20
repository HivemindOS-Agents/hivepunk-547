# duckophila-stated-facts: publish record

Status: publish package prepared in this folder. The live
Hub page was NOT fetched or confirmed in the step that
wrote this file, so every live entry below is an intended
value, not a confirmed one.

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

## Self-test output (last confirmed)

Runner: HivemindOS bee-self-test, 2026-11-20 03:42 UTC
Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44669522722
Result: passed

~~~text
built rows validate: 17 rows
every built row has a non-empty http(s) source_url, a known label and a unique fact
all rows use only the two allowed sources, and both appear
facts.csv matches the built rows (17 rows)
every committed row has a non-empty source_url
validator rejects empty/off-scheme source_url, unknown label and duplicate fact
self-test: all checks passed
~~~

This output was the runner's result for the pre-card
self-test; the extended self-test in this folder has not
yet been run by the runner, so its pass is unconfirmed.

## Left for owner

Owner: run the HivemindOS publish step to publish the two
files above, then fetch the live Hub page and edit this
file to replace the intended URL, file list and row count
with the confirmed ones and paste the fresh self-test
output.
