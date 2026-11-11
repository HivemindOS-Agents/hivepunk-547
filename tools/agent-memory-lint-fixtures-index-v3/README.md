# agent-memory-lint-fixtures-index-v3

A small, runnable CLI that validates an agent-memory-lint index JSON against
the five-file fixture layout and reports **missing**, **renamed** and
**extra** entries.

## Files

- `index_check.py` — the checker and CLI. Defines the canonical five files
  (`README.md`, `index.json`, `index.md`, `index_check.py`, `self_test.py`)
  and the three fixture directories (`clean/`, `bad-rows/`, `bad-card/`).
- `index.json`, `index.md` — this folder's own index pair.
- `sample_index.json`, `sample_index.md` — a clean sample pair (3 entries).
- `sample_bad_index.json` — a deliberately broken copy (renamed entry, extra
  entry, missing file) to demonstrate the failure paths.
- `self_test.py` — runs `index_check` on the three inputs and exits 0 only
  when all pass.

## Run

~~~
python3 index_check.py sample_index.json sample_index.md
python3 index_check.py sample_bad_index.json sample_index.md
python3 self_test.py
~~~

No arguments, no network, no writes. Works from inside this folder alone.

## What the CLI reports

For each entry: `ok` (matches a known fixture dir), `missing` (a known dir has
no entry), `renamed` (path is not known but its tail matches a known name),
or `extra` (matches nothing). It also checks JSON-vs-markdown agreement
(path set, rule, description, expected_exit_code) and prints
`verdict: OK` or `verdict: ISSUES(n)`. Exit 0 only when there are no issues.

## Untested

None of this was executed by the author of this folder; the HivemindOS runner's
`SELFTEST_OUTPUT.md` in this folder is the only record of a real run. The
canonical five filenames and three fixture dir names are taken from the earlier
`agent-memory-lint-fixtures-index-v2` index; the real fixture folders under
`tools/agent-memory-lint-fixtures/` were not re-measured, so the expected lint
exit codes (0, 1, 1) are recorded intent, not a measurement. If the real names
differ, update `FILES` and `FIXTURE_DIRS` in `index_check.py` and re-run.

## Not published

Nothing here is uploaded, posted or published by this folder. Publishing
happens only through the owner's publish play under the owner's account.

License: not stated — owner to choose.
