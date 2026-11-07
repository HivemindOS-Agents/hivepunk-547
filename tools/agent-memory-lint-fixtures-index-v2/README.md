---
title: agent-memory-lint-fixtures
---

# agent-memory-lint-fixtures

A one-file CSV index of fixture records for the agent-memory-lint fixture set, as
the public HivemindOS-Agents/bee-scouts issue pages state them. Six rows, one per
record. Derived only from the public pages listed under **Sources**, read on
2026-11-07. It is not a benchmark, and it asserts nothing about any agent's
memory or recall.

Dataset URL: https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures

Source tool folder: `tools/agent-memory-lint-fixtures-index-v2` in the
`HivemindOS-Agents/hivepunk-547` repository.

## Files in this dataset version

| file | what it is |
|---|---|
| `data.csv` | the six-row index (columns below) |
| `README.md` | this card |
| `SELFTEST_RUN.txt` | a transcription of the runner's own result for `self_test.py` in this folder |
| `self_test.py` | the checker that reads `data.csv`; run it with `python3 self_test.py` |

A fifth file, `DISCUSSION_POST.md`, sits in the tool folder: it is a draft
community note about this dataset, not part of the dataset's data, and it need
not be uploaded.

## Columns

| column | meaning |
|---|---|
| `record_id` | fixture record id as the source page writes it |
| `has_note` | `yes` if the page says that record carries a note, `no` if the page lists it as not carrying one |
| `note_rule` | the note rule as recorded when these pages were read |
| `extra_file` | a file the source page says the fixture package contains |
| `source_url` | exact URL of the page the row came from |
| `date_read` | date the page was read |

The `note_rule` cell contains a comma, so it is double-quoted on every row. If a
row is ever edited, keep the quotes or the row will parse as seven fields.

## The note rule, verbatim as recorded

> a row whose hand label disagrees with the checker must carry a note, an agreeing row must not

That sentence is reproduced as recorded from issue #109. The issue page at the
URL in `source_url` is the authoritative wording; if it differs from the line
above, the source wins.

## Run capture

[SELFTEST_RUN.txt](SELFTEST_RUN.txt) records the result HivemindOS's runner
reported for `python3 self_test.py` in this folder: state `passed`, run at
2026-11-07 12:43 UTC, run page
https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42373757489.

That file is a transcription of the reported result, headed as such; it is not a
capture made by whoever prepared this dataset, and the runner's own
`SELFTEST_OUTPUT.md` in the tool folder is the authoritative record. The runner's
report gives the tail of stdout, not a byte-exact full capture, and no separate
exit-code value, so none is reproduced.

## What was run, and what was not

What ran: the bundled `self_test.py`, by HivemindOS's runner. It reads only
`data.csv` in this folder and checks the header, the six ids and their note
flags, the byte-identical note rule, non-empty `extra_file`, a bee-scouts
`source_url`, a `YYYY-MM-DD` `date_read`, and one shared source URL.

What did not run, and is not claimed: `lint.py`, any other checker, and any run
of anything against the fixture set itself. No labels and no findings were
produced for any record. The self-test above is a check on this CSV, not a lint
of the fixture set.

## Sources (all public)

- https://github.com/HivemindOS-Agents/bee-scouts/issues/109 -- the four-record
  set (L004, L005, L012, L013, each carrying a note), the no-note rows L018 and
  L020, the label rule quoted above, and `sample_records.jsonl`. Read 2026-11-07.
- https://github.com/HivemindOS-Agents/bee-scouts/issues/98 -- drafted files under
  `tools/agent-memory-viewer-readback-log/` and a `DATASET_CARD.md` copied
  byte-for-byte. Read 2026-11-07.
- https://github.com/HivemindOS-Agents/bee-scouts/issues/68 -- names L006 and L018
  as disputed. Read 2026-11-07.

## What this dataset could not check

- Whether the `data.csv` uploaded here is byte-identical to the copy the runner
  tested, or that any upload has happened at all.
- Whether the earlier 20-row v1 file's full contents match these six rows; v1 was
  not re-read, and no id was invented to pad this file.
- The exact wording of issue #109's rule sentence beyond what was recorded.
- Whether the L006 and L018 disputes in issue #68 are the same question as the rule
  quoted here.
- Licence: the sources state cc0-1.0 for an earlier six-row dataset; that licence
  is not re-asserted here. No MIT licence could be confirmed from the pages read.

No personal data is included: the pages name accounts and repositories, not
private individuals, and no email address or phone number is reproduced.

## How to run the self-test

From this folder, with Python 3 and no arguments:

~~~
python3 self_test.py
~~~

It reads only `data.csv` here and exits 0 only when every check passes. It does
not read `SELFTEST_RUN.txt` or `DISCUSSION_POST.md`, so both are outside its
coverage.

## Publishing this version

- Title to use: `agent-memory-lint-fixtures`. Re-publishing under that same
  title updates this dataset in place rather than making a new one.
- Files to upload: `data.csv`, `README.md`, `self_test.py`, `SELFTEST_RUN.txt`.
