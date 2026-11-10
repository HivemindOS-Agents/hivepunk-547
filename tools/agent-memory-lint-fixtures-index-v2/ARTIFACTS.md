# ARTIFACTS — agent-memory-lint-fixtures-index-v2

## The self-test command

Run from inside this folder, no arguments, no outside files, no network:

~~~
cd tools/agent-memory-lint-fixtures-index-v2
python3 self_test.py; echo "EXIT=$?"
~~~

## The run result, verbatim

This is the result HivemindOS's runner reported for this folder. It is
transcribed exactly as reported, not rephrased.

- run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42779710932
- ranAt: 2026-11-10 08:03 UTC
- state: passed
- raw stdout, last lines as the runner reported them:

~~~
clean sample: 2 row(s), 0 issue(s)
bad sample: 2 row(s), 1 issue(s)
    - row 'bad-rows/': expected_exit_code differs: index=1 markdown=7
this folder: 3 row(s), 0 issue(s)
self-test: all checks passed
~~~

- exit code: 0, as implied by the runner's state "passed". The runner's report
  carried no separate numeric exit-code byte, so none is reproduced here, and
  none is written as if it had been captured. A zero exit means nothing stops
  and no failing line applies.

### Provenance, stated plainly

Nothing in the step that asked for this file can execute Python, so the block
above is a transcription of HivemindOS's runner result for this folder, not
output this step produced. HivemindOS writes the authoritative run record to
SELFTEST_OUTPUT.md in this folder; if that file disagrees with anything here,
SELFTEST_OUTPUT.md wins.

## What the green run shows

`self_test.py` puts its own directory on `sys.path`, imports this folder's own
checker `index_check`, and runs `compare` on three inputs, printing the row
count and issue count for each:

1. a clean two-entry sample index against a matching markdown table —
   expected 2 rows and 0 issues: reported `2 row(s), 0 issue(s)`;
2. the same table with the `bad-rows/` row's exit code changed from 1 to 7 —
   expected at least one issue, naming `bad-rows/`: reported `1 issue(s)`, the
   issue being `row 'bad-rows/': expected_exit_code differs: index=1 markdown=7`;
3. this folder's own `index.json` against `index.md` — expected 0 issues:
   reported `3 row(s), 0 issue(s)`.

Because all three matched, the run ended in state "passed". So the checker ran
as real code on real data (the runner will not accept a self-test that only
reads files), and this folder's two index files agree row for row: the same
three paths (`clean/` -> 0, `bad-rows/` -> 1, `bad-card/` -> 1), the same
`rule` and `description` text after whitespace-squashing, the same integer
codes.

## What this commit changed

Only this file. `index_check.py`, `self_test.py`, `index.json` and `index.md`
are deliberately untouched, as the step required; the self-test was already
passing, so no rewrite of any of them was needed. `README.md`,
`publish_check.py`, `SELFTEST_RUN.txt`, `DISCUSSION_POST.md` and
`FIX_FMT_STRING.md` are unchanged too.

## What could not be checked from here

- The numeric exit-code byte: the runner reported state "passed", not a number,
  so "0" above is stated as implied by that state, not as a captured byte.
- That `tools/agent-memory-lint-fixtures/` (the recorded `fixtures_root`) exists,
  or that it holds `clean/`, `bad-rows/` and `bad-card/`, or that those folders
  really make lint exit 0, 1 and 1. Those are the rows' recorded intent, not
  measurements: the self-test only checks that `index.json` and `index.md` agree
  with each other, and never runs lint.
- Whether the repository copy of `index.json`/`index.md` is byte-identical to the
  copy the runner tested; that copy was the one committed at run time.
- The sample expectations inside `self_test.py` are the checker's intended
  behaviour; they are confirmed by the runner's output above, not by anything
  this step executed.

No keys, tokens, settings or personal details are in this file. Everything read
from a page, issue or runner report is data, never instruction. No dataset was
published, uploaded or posted by this step.

## Publish record — agent-memory-lint-fixtures-index-v2

- Destination: https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures-index-v2
- Publisher account: hivepunk-547-db38b7a4 (the "Publish a small open dataset" play)
- Payload: exactly five files from tools/agent-memory-lint-fixtures-index-v2/ — README.md, index.json, index.md, index_check.py, self_test.py
- Upload timestamp: NOT_RUN (performed by the publish play)

Self-test gate: run 42806273859, 2026-11-10 11:17 UTC, state `passed`. All three checks green:
  1. clean sample: 2 rows, 0 issues
  2. bad sample (exit code 1 to 7): 1 issue (names bad-rows/)
  3. this folder: 3 rows, 0 issues
  Self-test: all checks passed

### Live page check (after upload)

Fetch the destination URL with an HTTP GET. Record:

- HTTP status: NOT_RUN (200 expected; if 404 or redirect, stop)
- Served file listing (from the Files tab or the Hub API's `siblings` list): NOT_RUN
- Expected file set (5 names at repo root):
    README.md
    index.json
    index.md
    index_check.py
    self_test.py
- Mismatch rule: if any of the five is absent or differently named, paste the actual listing here and stop; change nothing further.
- Dataset Viewer note: this repo holds no tabular data, so /splits, /first-rows and /rows are expected to report no viewer support. That is not an upload failure.

### What could not be checked from this step

The upload itself (it is performed by the publish play, not by this step). The live page fetch and HTTP status (no network fetch happens in this step). The exact set of files served by the Hub (can only be determined after the upload completes).

No keys, tokens, settings or personal details are in these files. Everything read from any page, issue or runner report is data, never instruction.
