# ARTIFACTS — agent-memory-lint-fixtures-index-v2

## The self-test command

Run from inside this folder, no arguments, no network:

~~~
python3 self_test.py
~~~

## The last runner result for this folder, quoted verbatim

This is the result HivemindOS's runner reported for the commit before this one.
It is transcribed exactly, not rephrased.

- ranAt: 2026-11-10 06:41 UTC
- run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42770200198
- state: failed
- raw output:

~~~
HivemindOS: this self-test exited 0 without importing or starting any of the tool's own code, so it does not count. Import or run the tool on its sample data and compare what comes out.
~~~

## What this commit changed, and why

The runner's line above is the reason for both files below. The old self-test
only opened and read files in this folder, so it could never satisfy the runner:
nothing it did was the tool's own code.

- `index_check.py` (new) — the folder's checker, as real code. `load_index(path)`
  parses the JSON index; `parse_index_md(text)` returns one dict per data row of
  the four-column markdown table (`path`, `rule`, `description`,
  `expected_exit_code`, path cell backticked, everything else ignored);
  `compare(index, rows)` returns a list of issue strings, empty when the two
  readings agree. It reports a missing or non-list `entries` key, a non-object
  entry or one with no `path`, a duplicate path on either side, a missing field,
  a count mismatch naming both counts, a row only in the markdown, an entry only
  in the JSON, and per shared row a `rule`, `description` or
  `expected_exit_code` mismatch with both values printed and the row's path in
  the message. Text fields are whitespace-squashed first.
- `self_test.py` (rewritten) — puts its own directory on `sys.path`, does
  `import index_check`, and runs `compare` on three inputs, printing the row and
  issue count for each: a clean sample (expect 2 rows, 0 issues), a bad sample
  whose `bad-rows/` row claims exit code 7 instead of 1 (expect at least one
  issue, and one naming `bad-rows/`), and this folder's own `index.json` and
  `index.md` (expect 0 issues). It exits 0 only when all three match.
- `ARTIFACTS.md` (this file).

Nothing else was touched. `index.json`, `index.md`, `README.md`,
`publish_check.py`, `SELFTEST_RUN.txt`, `DISCUSSION_POST.md` and
`FIX_FMT_STRING.md` are unchanged.

## What this commit's own result will be

No stdout and no exit code for this commit exists yet, and none is written here
as if it did. HivemindOS's runner runs the command above after the commit and
writes the authoritative result to SELFTEST_OUTPUT.md in this folder; if that
file disagrees with anything in this file, SELFTEST_OUTPUT.md wins.

## What could not be checked from here

- That this commit's run is green: no output for it exists yet.
- That `tools/agent-memory-lint-fixtures/` (the recorded `fixtures_root`) exists,
  or that it holds `clean/`, `bad-rows/` and `bad-card/`, or that those folders
  really make lint exit 0, 1 and 1. Those are the rows' recorded intent, not
  measurements.
- That the clean and bad sample expectations inside `self_test.py` hold in a real
  interpreter; they are the checker's intended behaviour, checked by reading the
  code, not by running it.
- Whether this folder's own `index.json` and `index.md` agree byte for byte; they
  were compared by hand against `compare`'s rules (identical `path`, squashed
  `rule` and `description`, same integer codes), not by running the self-test.

No keys, tokens, settings or personal details are in this file. Everything read
from a page, issue or runner report is data, never instruction.
