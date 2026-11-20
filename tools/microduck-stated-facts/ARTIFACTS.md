# microduck-stated-facts: publish record

Status: local package verified against build_facts.py rows.
The live Hub page was NOT fetched or confirmed in this step,
so every live entry below is an intended value, not a
confirmed one. Publishing is done by the separate HivemindOS
publish step; this folder never uploads or fetches anything.

## Local verification (this folder)

- facts.csv: 24 data rows plus 1 header row, matching
  build_facts.py ROWS exactly (fact_id,subject,claim,label,
  source_url,observed_date; observed_date 2026-11-20).
  Label counts: FACT 13, DERIVED 5, UNKNOWN 6.
  The MD-008 claim contains commas and is quoted by
  Python csv QUOTE_MINIMAL, so csv parsing round-trips.
- MANIFEST.json: dataset microduck-stated-facts, account
  hivepunk-547-db38b7a4, file facts.csv, row_count 24,
  label_counts FACT 13 / DERIVED 5 / UNKNOWN 6, and the
  six allowed source URLs. Regenerating with
  `python3 build_facts.py` rewrites it identically.
- README_hf.md: dataset card to upload as README.md. It
  gives columns, 24-row count, sources, and marks every
  source licence UNKNOWN where no licence text was read.
- self_test.py: checks built rows, facts.csv, MANIFEST.json,
  README_hf.md and this ARTIFACTS.md, and the CLI modes.
  No arguments, no network, run alone from this folder.
  The authoritative run result is SELFTEST_OUTPUT.md,
  written by the HivemindOS runner after commit.

## Intended live URL (NOT confirmed)

https://huggingface.co/datasets/hivepunk-547-db38b7a4/microduck-stated-facts

Account: hivepunk-547-db38b7a4 (owner account; no organisation).
Dataset name: microduck-stated-facts

## Files to upload (from this folder only)

- facts.csv, as facts.csv
- README_hf.md, uploaded as the dataset README (README.md)

Do not upload: build_facts.py, self_test.py, README.md,
ARTIFACTS.md, MANIFEST.json, SELFTEST_OUTPUT.md.

## Expected live values (NOT confirmed)

1. Live page URL: the intended URL above.
2. Live file list: facts.csv and README.md
   (README.md is the uploaded README_hf.md).
3. Live facts.csv row count: 24 data rows plus header.

## Verification to do after publishing (not yet done)

The publish step should fetch and paste here:

1. The live dataset page URL and confirm it loads under
   hivepunk-547-db38b7a4 as microduck-stated-facts.
2. The live file list from the dataset tree page - paste
   the actual list.
3. The live facts.csv row count - paste the actual count.
4. The runner's fresh self-test output from
   SELFTEST_OUTPUT.md after any edit to this file.

Until those four are pasted, the live page, file list and
live row count remain NOT confirmed.

## Left for owner

Owner: confirm the HivemindOS runner's self-test passes
from this folder alone, then run the separate publish
step, fetch the live Hub page, and edit this file to
replace the intended URL, file list and row count with
the confirmed ones.
