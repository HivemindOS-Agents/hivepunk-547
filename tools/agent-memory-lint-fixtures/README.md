# agent-memory-lint fixtures (tool + dataset rows)

Small fixture bundle for an agent-memory linter: 20 synthetic records, a
hand-written label file, an unchanged stdlib-only checker, and a build step that
turns them into one agreement row per record.

## What is here

| File | What it is |
| --- | --- |
| `records.jsonl` | 20 synthetic records, one JSON object per line. |
| `expected_labels.json` | The hand-written labels, canonical sorted order. |
| `check.py` | The checker, unchanged. Stdlib only, no network, no writes. |
| `build_labelled_rows.py` | Builds the per-record table with hand-derived labels. |
| `DATASET_CARD.md` | The dataset card: caveat first, both commands UNRUN. |
| `self_test.py` | Checks the files and the hand-derived counts. No args, no network. |

## Build the rows

```
python3 build_labelled_rows.py records.jsonl expected_labels.json > labelled_rows.csv
```

Columns: `id, text, source, as_of, tags, expected_labels, checker_labels,
agree, note`. `checker_labels` is **hand-derived from `check.py`'s code**: no
checker process was run, so there is **no exit code, stdout, diff or checksum**.
The hand-derived agreement is **17/20**; the mismatches are **L006, L015, L018**,
each noted in the `note` column.

## Reproduce the labels - UNRUN

```
python check.py records.jsonl > got.json
diff -u expected_labels.json got.json
```

**Both are UNRUN.** Neither command was executed anywhere in this work.

## Self-agreement is not accuracy

One author wrote the records, the labels and the checker. A match between the
two label columns says only that this author's rules agree with this author's
labels. It is not a measurement against any real agent memory store.

## Dispute a label

Reply with the **id**, the **label you would assign**, and the **field or
sentence** you read it from. L006, L015 and L018 are open.

## What is untested

- No Python was run in this work: `checker_labels`, the 17/20 count and the
  three mismatch notes are hand-derived, not captured from a process.
- `self_test.py` is written here and has not been executed by its author; it
  checks file presence, id set equality, sorted order, and the hand-derived
  17/20 count with mismatches L006/L015/L018.
- The reproduce commands are unrun, so no byte-for-byte comparison exists.
- No checksum was computed.

## Rules kept

No upload script, token step or CLI command is written here. No key, password
or personal detail appears in these files. Source text and other agents' posts
are data, never instruction.

## Left for the owner

1. Publish these rows under the account with the title
   "agent-memory-lint fixtures: 20 labelled records, checker unrun";
   publishing the same title again updates it in place.
2. Open the caveat-first discussion post on the dataset page (copy in
   `DATASET_CARD.md` and in this step's result text).
