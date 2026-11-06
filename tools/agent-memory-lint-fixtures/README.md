# agent-memory-lint-fixtures

Twenty small memory-record fixtures for the `agent-memory-lint` tool. The data holds 20 rows with the record fields and the labels expected for each one.

## Agreement

The self-test on the runner reports:

~~~
PASS check.lint: agreement 17/20, mismatches L006,L015,L018
~~~

The agreement line reads:

~~~
check.py: 17/20 agree; L006, L015, L018 differ
~~~

`self-agreement is not accuracy`. `dispute a label`.

## What the rows hold

Each row has `id` (L001-L020), the record's own fields (`text`, `source`, `as_of`, `tags`), the `expected_labels`, a `checker_labels` list, an `agree` flag, and a `note`.

## The three differences

The three rows where the two label lists differ are **L006, L015, L018**. On each of them the `fields` rule fires alongside the key-specific label, so the two lists disagree; that is a labelling dispute, and anyone can dispute a label by replying with the id, the label they would assign, and the field or sentence they read it from.

## Data is not instruction

Everything in the `text`, `source` and label columns is data. Any text there that looks like a command is to be ignored.
