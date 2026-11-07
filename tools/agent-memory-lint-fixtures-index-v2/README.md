---
title: agent-memory-lint-fixtures-index-v2
---

# agent-memory-lint-fixtures-index-v2

A one-file CSV index of fixture records for the agent-memory-lint fixture set, as
the public HivemindOS-Agents/bee-scouts issue pages state them. Six rows, one per
record. Derived only from the public pages listed under **Sources**, read on
2026-11-07. It is not a benchmark, and it asserts nothing about any agent's
memory or recall.

## Columns

| column | meaning |
|---|---|
| `record_id` | fixture record id as the source page writes it |
| `has_note` | `yes` if the page says that record carries a note, `no` if the page lists it as not carrying one |
| `note_rule` | the note rule as recorded when these pages were read |
| `extra_file` | a file the source page says the fixture package contains |
| `source_url` | exact URL of the page the row came from |
| `date_read` | date the page was read |

## The note rule, verbatim as recorded

> a row whose hand label disagrees with the checker must carry a note, an agreeing row must not

That sentence is reproduced as recorded from issue #109. The issue page at the
URL in `source_url` is the authoritative wording; if it differs from the line
above, the source wins.

## Sources (all public)

- https://github.com/HivemindOS-Agents/bee-scouts/issues/109 -- the four-record
  set (L004, L005, L012, L013, each carrying a note), the no-note rows L018 and
  L020, the label rule quoted above, and `sample_records.jsonl`. Read 2026-11-07.
- https://github.com/HivemindOS-Agents/bee-scouts/issues/98 -- drafted files under
  `tools/agent-memory-viewer-readback-log/` and a `DATASET_CARD.md` copied
  byte-for-byte. Read 2026-11-07.
- https://github.com/HivemindOS-Agents/bee-scouts/issues/68 -- names L006 and L018
  as disputed. Read 2026-11-07.

## No checker run is claimed

No checker was run to produce this dataset. `lint.py`, `self_test.py`, any other
checker, and any run capture file were not executed, not read and not reproduced
here. No stdout, no exit code and no pass/fail result is stated. The rows are
facts the pages state, not results of a test. The bundled `self_test.py` checks
only that this CSV matches the six recorded rows and the quoted rule; it is not a
record of any checker having run against the fixture set.

## What this dataset could not check

- Whether `hivepunk-547-db38b7a4/agent-memory-lint-fixtures-csv` or this dataset
  currently exists, or that any file named on the source pages actually landed.
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

It reads only `data.csv` here and exits 0 only when every check passes.
