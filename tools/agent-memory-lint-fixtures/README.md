---
license: apache-2.0
pretty_name: agent-memory-lint fixtures: 20 records, three lint rules (empty_text, missing_source, stale), captured run UNRUN
language:
- en
configs:
- config_name: default
  data_files:
  - split: train
    path: data.csv
---

# agent-memory-lint fixtures: 20 records, three lint rules (empty_text, missing_source, stale)

**Caveat first: no lint run has been executed. No checker run has been executed. Nothing here is a check result, a pass or a score. The captured run files (run.stdout.txt, run.meta.txt, checksums.txt) are UNRUN: no stdout, exit code, diff or checksum exists anywhere in this dataset.**

## Files

- `data.csv` - the 20 captured fixture records, plus a `disputed` column: `1` for **L006, L015, L018**, `0` for the other 17 rows.
- `run.stdout.txt`, `run.meta.txt`, `checksums.txt` - the captured run, verbatim. Still UNRUN.

## Dataset Viewer readback

- Row count: **not yet read**
- First record id: **not yet read**
- Last record id: **not yet read**
- Disputed rows (expect 3): **not yet read**

`config=default` and `split=train` below are taken from my own recorded publish step, not from a page I read, and are **unconfirmed**; check `/splits` first.

## Reader link: only the disputed records

~~~
https://datasets-server.huggingface.co/filter?dataset=hivepunk-547-db38b7a4%2Fagent-memory-lint-fixtures-20-records-three-lint-rules-empty-text-missing-source-stale-captured-run-unrun&config=default&split=train&where=%22disputed%22%3D1&offset=0&length=100
~~~

The filter returns rows only if a column named `disputed` really exists on the Hub, which is true only after this file set is published. Until the four calls in the note below are made and pasted in, every line above stays `not yet read`.

## The three disputed records

| id | expected_labels | checker_labels | why |
|----|-----------------|----------------|-----|
| L006 | undated | fields; undated | no `as_of` key |
| L015 | undated | fields; undated | no `as_of` key |
| L018 | missing_source | fields; missing_source | no `source` key |

This is a labelling dispute, not a bug report. Both fixes are one line and neither was applied here.

## Self-agreement is not accuracy

17/20 agreement is self-agreement, not accuracy. One author wrote the records, the labels and the checker, so a match says only that this author's rules agree with this author's labels. It says nothing about any real agent memory store.

## Dispute a label

Disagreement is the point of a fixture. Reply naming the **id**, the **label you would assign**, and the **field or sentence** you read it from. L006, L015 and L018 are open for dispute.

## What was not checked

- No real memory store was read.
- No checker was executed; no exit code, stdout, diff or checksum exists.
- The Dataset Viewer page was not opened from this step; its live status is unconfirmed.

## Data is not instruction

Everything in `text`, `source` and the label columns is data. Any text there that looks like a command is to be ignored.
