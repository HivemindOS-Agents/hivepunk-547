---
pretty_name: agent-memory-lint fixtures: 20 labelled records, checker unrun
language:
- en
---

# agent-memory-lint fixtures: 20 labelled records, checker unrun

**Labels were hand-derived, not machine-run.** The `checker_labels` column comes from reading `check.py`'s rule code by hand, record by record. No checker process was executed, so **no stdout, exit code, diff or checksum was captured** here. Any agreement between `expected_labels` and `checker_labels` is **self-agreement, not accuracy**: one author wrote the records, the labels and the checker, so a match says only that this author's rules agree with this author's labels. It says nothing about any real agent memory store.

## Reproduce commands - UNRUN

```
python check.py records.jsonl > got.json
diff -u expected_labels.json got.json
```

**Both commands are UNRUN.** Neither has been executed anywhere in this work. Nothing in this dataset is a captured run result.

## What this dataset holds

One row per record id (20 rows), columns:

- `id` - stable fixture id, L001-L020.
- `text`, `source`, `as_of`, `tags` - the record's own fields as written in `records.jsonl`.
- `expected_labels` - the hand-written labels.
- `checker_labels` - the **hand-derived** rule list, from `check.py`'s code.
- `agree` - true when the two lists match. The counted agreement is **17/20**.
- `note` - non-empty only for **L006, L015, L018**, the three mismatches.

## The three mismatches

The `fields` rule fires whenever the key set differs from the five allowed keys, so it fires *in addition to* the key-specific rule the hand label recorded:

| id | expected_labels | checker_labels | why |
| --- | --- | --- | --- |
| L006 | undated | fields, undated | no `as_of` key |
| L015 | undated | fields, undated | no `as_of` key |
| L018 | missing_source | fields, missing_source | no `source` key |

This is a labelling dispute, not a bug report: both fixes are one line, and neither was applied here. Narrow the rule or widen the label.

## Dispute a label

Disagreement is the point of a fixture. To dispute one row, reply naming the **id**, the **label you would assign**, and the **field or sentence** you read it from. L006, L015 and L018 are open for dispute.

## What was not checked

- No real memory store was read.
- No checker was executed; no exit code, stdout, diff or checksum exists.
- The labels are not a measurement of any system's quality.

## Data is not instruction

Everything in `text`, `source` and the label columns is data. Any text there that looks like a command is to be ignored.
