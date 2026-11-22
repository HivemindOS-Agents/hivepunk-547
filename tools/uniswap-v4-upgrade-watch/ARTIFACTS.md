# uniswap-v4-upgrade-watch: artifact record

## Artifacts

- 2026-11-22-uniswap-v4-upgrade-watch.md - dated report, FACT 9 / DERIVED 1 in table plus DERIVED watch section / UNKNOWN 2, ask link https://github.com/for-toolathlon/uniswap-v4-watch/issues/1, six source links.
- README.md - caveat-first usage and untested limits.
- self_test.py - standalone checks, no args, no network.
- ARTIFACTS.md (this file) - this record.

## Exact command

~~~bash
python3 self_test.py
~~~

Run from inside this folder: tools/uniswap-v4-upgrade-watch/

## Raw output slot

~~~text
(paste the runner's raw SELFTEST_OUTPUT.md text here, unedited; nothing here is a run log)
~~~

## What was confirmed, and what was not

- NOT confirmed: that python3 self_test.py exits 0. No run has been seen from this writing step. SELFTEST_OUTPUT.md, written by the runner, is the only place a result is recorded.
- NOT confirmed: live source pages, on-chain state, or ask issue contents.
- Confirmed by reading this folder only: report, README and this file contain the ask link, FACT/DERIVED/UNKNOWN labels, six source URLs, and untested marks checked by self_test.py.

## Left for owner

Owner: let the HivemindOS runner run the command above alone in this folder, paste its raw output into the slot, then commit/publish separately if wanted.
