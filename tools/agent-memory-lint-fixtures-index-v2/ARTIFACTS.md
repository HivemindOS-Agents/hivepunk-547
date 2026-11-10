# ARTIFACTS — agent-memory-lint-fixtures-index-v2

## The self-test command

Run from inside this folder, no arguments, no network:

~~~
python3 self_test.py
~~~

## Raw stdout and exit code

Nothing in this step can execute Python, so the self-test was not run here and
no stdout line or exit code is written as if it had been. HivemindOS's runner
runs the command above after each commit and writes the authoritative result to
SELFTEST_OUTPUT.md in this folder; if that file disagrees with anything below,
it wins.

The last runner result recorded for this folder, quoted verbatim, is from the
commit before this one:

- ranAt: 2026-11-10 06:07 UTC
- run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42766400078
- state: failed
- raw last line:

~~~
FAIL: index.json not found
~~~

That run stopped at the first check because index.json was absent. This commit
adds index.json, and the index.md it must match row for row; the next runner
pass supplies this commit's stdout and exit code.

## What this commit changed

- `index.json` (new): top-level `entries`, `dataset`, `repository`,
  `fixtures_root`; three entries — `clean/` to 0, `bad-rows/` to 1,
  `bad-card/` to 1 — each with `path`, `rule`, `description`,
  `expected_exit_code`.
- `index.md` (new): the same three rows in the same order, the same rule text
  and the same expected codes, in the table shape `self_test.py` parses.
- `ARTIFACTS.md` (this file).

Nothing else was touched. `self_test.py`, `README.md`, `publish_check.py`,
`SELFTEST_RUN.txt`, `DISCUSSION_POST.md` and `FIX_FMT_STRING.md` are unchanged.

## What could not be checked

- That this commit's run is green: no stdout or exit code for it exists yet,
  and none is claimed here.
- That `tools/agent-memory-lint-fixtures/` (the recorded `fixtures_root`)
  exists, or that it holds `clean/`, `bad-rows/` and `bad-card/`; those folders
  were not read from here.
- That those folders really make lint exit 0, 1 and 1; those are the intended
  values recorded in the rows, not measurements.
- `README.md` was not re-read in this commit, so that it contains the `dataset`
  and `repository` strings `index.json` names is only as the earlier file
  listing showed.
