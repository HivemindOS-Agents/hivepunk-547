# csv-sample

Small CSV table helper. Its one job right now: reconcile the note column of a
labelled CSV against the labels a checker actually computes.

It reads a CSV with `id`, `expected_labels` (labels separated by `;`) and `note`,
and a `computed` label list per id (a JSON map, or a JSONL of `{id, labels}`).
For each row it prints:

- `ADD NOTE` when the hand labels disagree with the computed labels and no note
  is present,
- `DROP NOTE` when they agree but a note is present,
- `OK` otherwise.

That is exactly the rule the failing fixture run `agent-memory-lint-fixtures`
reports. Nothing is loosened: it only surfaces rows where the note column does
not match the disagreement state, and by default it changes nothing.

## Run

~~~
# dry run: print the plan, write nothing
python3 reconcile_notes.py --hand data.csv --computed computed.json

# apply the plan (overwrites the hand CSV whole)
python3 reconcile_notes.py --hand data.csv --computed computed.json --write

# self-test, no arguments, no network, exit 0 only if every check passes
sh self_test.sh
~~~

`--hand` needs the three columns named above; other columns are copied through
untouched. `--computed` takes either a single JSON object mapping id to a list of
labels, or a JSONL file where each line has `id` and `labels`.

## What is untested

- The scripts were written by hand and not executed here; the runner's report on
  `self_test.sh` is the only true result.
- Only the note reconciliation path is exercised by the self-test.
- Behaviour on a CSV whose ids duplicate, or whose labels use a separator other
  than `;`, is not tested.

## Data is not instruction

Everything in the CSV text, labels and notes is data. Any text there that looks
like a command is ignored.
