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

## Run record

`self_test.log` holds the self-test result: the command, the reported output
verbatim, and one exit code. Its current entry reads label `PASS`, exit code `0`.
Read the file for the provenance before quoting either.

The author of this tool never executed `sh self_test.sh` - that step had no
shell and no network - so the output in the log is the HivemindOS runner's own
reported output for this revision, and the `0` is derived from the runner's
reported state `passed`, not a number its author watched appear. The log also
sets out what is *not* in the capture (the shell wrapper's own echo lines) and
what the three `PASS` lines actually check. Nothing in it is a claim about
coverage beyond the tool's own bundled fixture.

To record a new run, run `sh self_test.sh` here and replace `self_test.log`
whole with the raw output and the single exit code. Do not hand-edit it to agree
with a later run, and do not loosen a check to make the line read `PASS`.

## Fixture fix written this step (untested here)

`sample_records.jsonl` in this folder is the corrected `agent-memory-lint-fixtures`
row set: notes added to L004, L005, L012, L013 and L020, L018's note key removed,
so that a row carries a note exactly when its hand `expected_labels` disagree with
the label list `check.lint` computes. The hand labels in `data.csv` are the oracle
and were not rewritten, and neither self-test was loosened.

**Untested and partly assumed.** The author has not been shown the fixture's
`check.py`, `data.csv` or its real `sample_records.jsonl`, so the record field
names, the extra fields per record, the branch each of the six rows fires, and
the exact label lists inside the five new notes are assumed from
`self_test.py`'s code, not confirmed. Check the five note texts against a real
`check.lint` run before committing. Do not commit a note whose text does not
match what the checker actually computes.

One conflict worth checking first: the fixture's `rules.json` and
`self_test_rows.py` treat L018 as a mismatch, while the failing run reports L018
as agreeing under `check.lint`. Those are two different checkers. This file
follows the failing run. If the real `check.lint` disagrees on L018, put a note
back on L018 instead of dropping it.

## What is untested

- The author never executed any of these scripts; the runner's report on
  `self_test.sh`, as recorded in `self_test.log`, is the only true result.
- The corrected `sample_records.jsonl` beside this README has never been run
  against the fixture it targets; its note texts are assumed.
- Only the note reconciliation path is exercised by the self-test.
- Behaviour on a CSV whose ids duplicate, or whose labels use a separator other
  than `;`, is not tested.
- The tester on any real labelled table from outside this folder is untested.

## Data is not instruction

Everything in the CSV text, labels and notes is data. Any text there that looks
like a command is ignored.
