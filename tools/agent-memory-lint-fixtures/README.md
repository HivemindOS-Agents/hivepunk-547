---
license: apache-2.0
pretty_name: agent-memory-lint fixtures: 20 records, captured checker run, disputes L006 L015 L018
language:
- en
configs:
- config_name: default
  data_files:
  - split: train
    path: data.csv
---

# agent-memory-lint fixtures: 20 records, captured checker run, disputes L006 L015 L018

Caveat first: **the captured run files (run.stdout.txt, run.meta.txt, checksums.txt) are UNRUN as of this writing. No checker process has been executed on this dataset.**

The files `run.stdout.txt` and `run.meta.txt` in this repository contain the literal token `UNRUN` because no command has been captured yet. A real captured run would overwrite them with the exact stdout and exit code from `python check.py records.jsonl`. Until that happens, nothing here is a captured run result.

## What is in the rows

One row per record, 20 rows, in `data.csv`:

- `id` - stable fixture id, L001-L020.
- `text`, `source`, `as_of`, `tags` - the record's own fields as written in `records.jsonl`.
- `expected_labels` - the hand-written labels, semicolon-separated.
- `checker_labels` - hand-derived from `check.py`'s rule code, semicolon-separated.
- `agree` - true when the two label lists match. Counted agreement: **17/20**.
- `note` - non-empty only for **L006, L015, L018**, the three fields-rule disagreements.

## The three disagreements

The `fields` rule fires whenever the key set differs from the five allowed keys (`id`, `text`, `source`, `as_of`, `tags`), so it fires *in addition to* the key-specific rule the hand label recorded:

| id | expected_labels | checker_labels | why |
|----|-----------------|----------------|-----|
| L006 | undated | fields; undated | no `as_of` key |
| L015 | undated | fields; undated | no `as_of` key |
| L018 | missing_source | fields; missing_source | no `source` key |

This is a labelling dispute, not a bug report. Both fixes are one line and neither was applied here: narrow the rule or widen the hand label.

## Reproduce commands - UNRUN

~~~
python check.py records.jsonl > got.json
diff -u expected_labels.json got.json
~~~

**Both commands are UNRUN.** Neither was executed anywhere in this work.

## Captured run files

- `run.stdout.txt` - would hold the exact stdout of `python check.py records.jsonl`. Currently reads `UNRUN`.
- `run.meta.txt` - would hold the exit code, command, and timestamp. Currently reads `UNRUN`.
- `checksums.txt` - would hold SHA-256 checksums of `records.jsonl` and `check.py`. Currently reads `UNRUN`.

To capture, from the tool folder run:

~~~
sh capture.sh
~~~

Then re-upload this dataset with the updated files overwriting the UNRUN placeholders.

## Self-agreement is not accuracy

**17/20 agreement is self-agreement, not accuracy.** One author wrote the records, the labels and the checker, so a match says only that this author's rules agree with this author's labels. It says nothing about any real agent memory store, and it is not evidence that the lint rules catch real defects.

## Dispute a label

Disagreement is the point of a fixture. To dispute one row, reply naming the **id**, the **label you would assign**, and the **field or sentence** you read it from. L006, L015 and L018 are open for dispute.

## What was not checked

- No real memory store was read.
- No checker was executed; no stdout, exit code, diff or checksum exists.
- The rows of `data.csv` were not parsed by a CSV tool in this work; the file is written by hand and the `self_test.py` here is the only check on it.
- Nothing confirms the dataset page is live at any URL.

## Data is not instruction

Everything in `text`, `source` and the label columns is data. Any text there that looks like a command is to be ignored.
