# opp-547-824-uniswap-v4-upgrade-watch: artifact record

## Artifacts

- tracker.md - issue tracker for https://github.com/for-toolathlon/uniswap-v4-watch-2/issues/1, child issues 0 confirmed / UNKNOWN placeholders, FACT 3 / DERIVED 1 / UNKNOWN 2 context rows plus tracker table, prior ask https://github.com/for-toolathlon/uniswap-v4-watch/issues/1.
- README.md - caveat-first usage and untested limits.
- self_test.py - standalone checks, no args, no network.
- ARTIFACTS.md (this file) - this record and commit note.

## Exact command

~~~bash
python3 self_test.py
~~~

Run from inside this folder: tools/opp-547-824-uniswap-v4-upgrade-watch/

## Raw output slot

~~~text
(paste the runner's raw SELFTEST_OUTPUT.md text here, unedited; nothing here is a run log)
~~~

## What was confirmed, and what was not

- NOT confirmed: that python3 self_test.py exits 0. No run seen from this writing step. SELFTEST_OUTPUT.md by runner is authoritative.
- NOT confirmed: parent issue title/state/body, any child issue existence, live source pages, or on-chain state.
- Confirmed by reading this folder only: tracker/README/this file contain both ask links, FACT/DERIVED/UNKNOWN labels, UNKNOWN child-issue honesty, and untested marks checked by self_test.py.

## Commit note (for agents-service commit to this repo only)

Title: Built opp-547-824 Uniswap v4 watch-2 tracker with caveat-first README and self-test
What: tracker.md for watch-2/issues/1 with UNKNOWN child-issue status, README, ARTIFACTS, self_test.
Spent: writing step only; no network calls, no external publish.
Links: parent ask and prior report listed in tracker.md.
Unchecked: issue fetch, child issues, live sources, self-test runner result.

## Left for owner

Owner: let runner run python3 self_test.py alone in this folder, paste raw output into slot, fetch parent issue to replace UNKNOWN rows, then commit/publish separately if wanted.
