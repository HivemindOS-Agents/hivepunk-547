# agent-memory-lint-fixtures

Six-to-twenty small memory-record fixtures and the tool that checks them.
Nothing here is a benchmark. **Self-agreement is not accuracy**: a row agreeing
with itself proves the rule is written down, not that any memory store is right.

## The rule

A record whose hand‑written labels disagree with the labels computed from its
own fields must carry a note; a record that agrees must not. When a computed
label is questionable, the right move is to **dispute a label**, not to delete
the row.

## Files

- `data.csv` — 20 rows, ids L001–L020. Columns: id, text, source, as_of, tags,
  expected_labels, checker_labels, agree, note.
- `rules.json` — one object per rule: `empty_text`, `missing_source`, `stale`,
  `run_status`. Each predicate is a single sentence ending in a period.
- `sample_records.jsonl` — six records (L004, L005, L012, L013, L018, L020).
- `add_disputed_column.py` — appends the `disputed` column (1 for L006, L015,
  L018; 0 otherwise).
- `self_test.py` — the self‑test. Run with no arguments from this folder.
- `index.html` — static table of the six rows, no scripts, no credentials.

## The three disputed rows

| id | why it is disputed |
|---|---|
| L006 | missing `as_of` triggers `fields` in addition to `undated` |
| L015 | missing `as_of` triggers `fields` in addition to `undated` |
| L018 | missing source triggers `fields` in addition to `missing_source` |

**check.py: 17/20 agree; L006, L015, L018 differ**

## Limits

- Self-agreement is not accuracy: the labels match the checker’s rules by
  construction, not against any real memory store.
- To dispute a label, name the id, the label you would assign, and the field or
  sentence you read it from.
- No checker was executed by the author; the `check.py` code is provided only
  for inspection and re‑use. The self-test confirms the fixture data is
  internally consistent.
