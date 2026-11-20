# microduck-stated-facts: publish record

Status: facts.csv regenerated in this folder to match
build_facts.py's built rows exactly, MANIFEST.json checked
against the built rows, and self_test.py corrected so its
CLI check matches build_facts.py's actual interface. The
live Hub page was NOT fetched or confirmed in this step,
so every live entry below is an intended value, not a
confirmed one.

## Regenerated files

- facts.csv: 24 data rows plus 1 header row, generated to
  match build_facts.py ROWS (fact_id,subject,claim,label,
  source_url,observed_date; observed_date 2026-11-20).
  Regeneration uses Python csv QUOTE_MINIMAL, as in
  build_facts.render(): the MD-008 claim contains commas
  ("software, simulators, policies and agent tools") and
  is therefore quoted in the file. The previous version
  had that claim unquoted, so csv parsing split it into
  extra fields and facts.csv did not match the built
  rows. Label counts: FACT 13, DERIVED 5, UNKNOWN 6.
- MANIFEST.json: unchanged; it already matches the built
  rows (dataset microduck-stated-facts, account
  hivepunk-547-db38b7a4, file facts.csv, row_count 24,
  the same label counts and the six allowed source URLs
  in build_facts.py order). Regenerating with
  `python3 build_facts.py` rewrites it identically.
- self_test.py: one check corrected. It previously
  called build_facts with no arguments and expected
  exit 2, but no-argument is build_facts.py's write mode
  (exit 0). The check now calls an unknown argument and
  expects exit 2. No other check changed.

## Intended live URL

https://huggingface.co/datasets/hivepunk-547-db38b7a4/microduck-stated-facts

Account: hivepunk-547-db38b7a4 (owner account; no organisation).
Dataset name: microduck-stated-facts

## Files to upload (from this folder only)

- facts.csv
- README_hf.md, uploaded as the dataset README (README.md)

Do not upload: build_facts.py, self_test.py, README.md,
ARTIFACTS.md, MANIFEST.json, SELFTEST_OUTPUT.md.

## Self-test run output

Not recorded here by the writer: nothing in this step was
run, so no run output or pass line is written into this
file. The authoritative result is SELFTEST_OUTPUT.md,
written by the HivemindOS runner after this commit, when
it runs `python3 self_test.py` alone from this folder
(after `python3 build_facts.py` has regenerated
facts.csv and MANIFEST.json). That run is expected to
check the regenerated facts.csv against the built rows
and MANIFEST.json row_count 24. Until the runner's
output appears in SELFTEST_OUTPUT.md, the standalone
self-test result remains NOT confirmed.

## Verification to do after publishing (not yet done)

The publish step should fetch and paste here:

1. The live dataset page URL (expected: the intended URL
   above) and confirm it loads under
   hivepunk-547-db38b7a4 as microduck-stated-facts.
2. The live file list from the dataset tree page
   (expected: facts.csv and README.md, where README.md is
   the uploaded README_hf.md) - paste the actual list.
3. The live facts.csv row count (expected: 24 data rows
   plus header) - paste the actual count.
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
