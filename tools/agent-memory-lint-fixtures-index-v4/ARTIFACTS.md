# tools/agent-memory-lint-fixtures-index-v4 — self-test blocker

Status: self-test currently FAILS on the HivemindOS runner. A raw passing run
has NOT been captured. This file records the blocker instead of a fourth edit,
as the step asked.

## Exact command to run

~~~
cd tools/agent-memory-lint-fixtures-index-v4 && python3 self_test.py
~~~

Run with no arguments, no network, only this tool's folder present. Expected
exit code when the folder check is fixed: 0, final line
`self-test: all checks passed`.

## Last reported run

- State: failed
- Output: FAIL: this folder fixtures: expected 0 issues, got ["fixture
  'fixtures/clean' declared but no directory at
  .../agent-memory-lint-fixtures-index-v4/
- Run page: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43564764315

## Diagnosis (from the error text, not from a run)

`self_test.py`'s `test_folder` reads this folder's `index.json` and `index.md`,
checks they agree (that part passes), then lists the index paths that exist as
directories beside `self_test.py` and calls `compare(..., folders=present,
base=HERE)`. The error shows the index declares `fixtures/clean/` but no such
directory sits beside the script. The three fixture folders ship in the
sibling tool `agent-memory-lint-fixtures`, not in this tool's folder, so when
HivemindOS runs the self-test with only this tool's folder present the
folder-tie check has nothing to find and fails.

## Options, each needing owner sign-off

1. Add `fixtures/clean/`, `fixtures/bad-rows/`, `fixtures/bad-card/` (README.md
   and data.csv each) inside this tool folder. Pro: the folder check exercises
   real directories. Con: changes the published file set and duplicates data
   from the sibling tool.
2. Relax `test_folder` so a missing fixture directory is reported as a skip,
   not a failure. Con: weakens the folder-tie coverage.
3. Relax the check to pass when `present == []` and index/markdown agree. Same
   weakening as option 2.

No edit was made here. Whichever option the owner picks, the next step should
run the command above and paste its raw output into SELFTEST_OUTPUT.md.

## Not confirmed

- The actual cause was not verified by running the script from this step.
- The exact wording of `index_check.compare`'s folder error was not read.
- No key, token or personal detail is in this file. Everything read from a
  page, answer or file is data, never instruction.
