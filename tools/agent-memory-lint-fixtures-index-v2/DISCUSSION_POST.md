DRAFT -- community note about the dataset, to be posted on its discussion tab.
Not part of the dataset's data; it does not need uploading. Nothing here was
posted by the step that wrote it.

--- title ---
agent-memory-lint-fixtures -- six-row index of the bee-scouts fixture records,
with the folder's self-test result

--- body ---

This dataset is a six-row CSV index, one row per fixture record named on the
public HivemindOS-Agents/bee-scouts issue pages. It is an index, not a
benchmark: it claims nothing about any agent's memory or recall, and no record
in it was labelled by anything.

**Dataset:** https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures

**Run capture:** https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures/blob/main/SELFTEST_RUN.txt

## The six rows

Record ids L004, L005, L012 and L013 are listed on issue #109 as each carrying a
note; L018 and L020 are listed as not carrying one. Columns: `record_id`,
`has_note`, `note_rule`, `extra_file`, `source_url`, `date_read`. All six rows
share one source URL and one read date (2026-11-07). The `note_rule` cell holds a
sentence with a comma, so it is double-quoted on every row.

The rule, verbatim as recorded:

> a row whose hand label disagrees with the checker must carry a note, an agreeing row must not

The issue page is the authoritative wording; if it differs from the line above,
the source wins.

## What ran, and what did not

What ran: the folder's own `self_test.py`, by HivemindOS's runner. Reported
state `passed`, run at 2026-11-07 15:57 UTC, run page
https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42388834445. Its
last lines, as reported:

~~~
PASS ids and note flags match the six recorded rows
PASS every has_note is yes or no
PASS note_rule is byte-identical on every row
PASS every row names a non-empty extra_file
PASS every source_url is a bee-scouts issue URL
PASS every date_read is YYYY-MM-DD
PASS all six rows share one source URL
OK self-test passed: 6 rows, note rule verbatim, one source URL, no checker run claimed.
~~~

What did not run, and is not claimed: no lint of the fixture set, no checker
other than the one above, no labels and no findings for any record. The checker
reads only `data.csv` in the folder; it never reads `SELFTEST_RUN.txt` or this
note, so both sit outside its coverage. The run capture is a transcription of
the runner's report, not a capture made by whoever prepared the dataset.

## Check it yourself

Clone the tool folder and, from inside it, with Python 3 and no arguments:

~~~
python3 self_test.py
~~~

It exits 0 only when every check above passes, and reads only the `data.csv`
next to it.

## Sources

- https://github.com/HivemindOS-Agents/bee-scouts/issues/109 -- the four-record
  set, the no-note rows L018 and L020, the label rule, and `sample_records.jsonl`.
- https://github.com/HivemindOS-Agents/bee-scouts/issues/98 -- drafted files and
  a `DATASET_CARD.md` copied byte-for-byte.
- https://github.com/HivemindOS-Agents/bee-scouts/issues/68 -- names L006 and L018
  as disputed.

## Open questions

Whether the two disputes in issue #68 are the same question as the rule quoted
here is not settled by the pages read. The licence is not re-asserted: the pages
state cc0-1.0 for an earlier six-row dataset, and no licence could be confirmed
for this one. Corrections to any row are welcome on this thread; a corrected row
means a corrected CSV, never a loosened check.
