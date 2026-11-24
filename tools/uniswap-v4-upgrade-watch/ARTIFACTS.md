# uniswap-v4-upgrade-watch: artifact record

## Artifacts

- seed_row.json - Uniswap/v4-core seed row: verified latest release tag/date UNKNOWN, unverified v4.0.0/2025-01-23 claim separate, source_url https://api.github.com/repos/Uniswap/v4-core/releases/latest.
- README.md - caveat-first usage and untested limits.
- self_test.py - standalone checks, no args, no network.
- ARTIFACTS.md (this file) - this record, exact command, raw exit-0 output and commit note.

## Exact command

~~~bash
python3 self_test.py
~~~

Run alone from inside this folder: tools/uniswap-v4-upgrade-watch/

## Raw stdout, stderr and exit code

Raw output from the latest HivemindOS runner run of the exact command above, pasted unedited. State: passed, ranAt: 2026-11-24 07:21 UTC, run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45347241694. This writing step made no new run; a re-run after this update is UNTESTED here and its new SELFTEST_OUTPUT.md is authoritative.

~~~text
seed_row.json: verified UNKNOWN, unverified v4.0.0/2025-01-23 separate, sources present
README has caveats first, untested marks, command, UNKNOWN honesty
ARTIFACTS.md records artifacts, command, verification slot, NOT confirmed, commit note, left-for-owner
self-test: all checks passed
exit code: 0
~~~

stderr was empty in that run (no FAIL line). Verification output slot: paste verified latest release tag/date here only after reading https://api.github.com/repos/Uniswap/v4-core/releases/latest verbatim; until then they stay UNKNOWN in seed_row.json.

## What was confirmed, and what was not

- Confirmed by the latest runner run above: python3 self_test.py exited 0 with the stdout shown.
- NOT confirmed: latest release tag/date from https://api.github.com/repos/Uniswap/v4-core/releases/latest. Seed row keeps UNKNOWN; v4.0.0 / 2025-01-23 is an unverified claim kept separate.
- NOT confirmed: re-run exit code after this commit's update (ARTIFACTS.md raw-output refresh and README run reference updated, no check logic changed). The runner's new SELFTEST_OUTPUT.md is the only evidence for that run.
- NOT confirmed: prior contents of this folder beyond the files written here.
- Confirmed by writing this folder only: seed_row.json, README.md, self_test.py and this file contain the exact command, raw exit-0 output, caveats and untested marks.

## Commit note (for agents-service commit to this repo only)

Title: Refresh uniswap-v4-upgrade-watch ARTIFACTS with latest exit-0 runner output (45347241694), keep UNKNOWN
What: Updated only tools/uniswap-v4-upgrade-watch/: ARTIFACTS.md now pastes the raw exit-0 output from run 45347241694, README.md references that run and marks live-API parts UNTESTED, seed_row.json keeps verified tag/date UNKNOWN pointing at https://api.github.com/repos/Uniswap/v4-core/releases/latest, self_test.py unchanged.
Spent: writing step only; no shell run, no network calls, no external publish.
Links: https://github.com/Uniswap/v4-core and https://api.github.com/repos/Uniswap/v4-core/releases/latest listed in seed_row.json; unverified claim source https://github.com/for-toolathlon/uniswap-v4-watch-3/issues/1; latest run https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45347241694.
Unchecked: live API verification, re-run exit code after this commit.

## Left for owner

Owner: let the runner re-run python3 self_test.py alone in this folder and compare its new SELFTEST_OUTPUT.md with the raw output above, verify the live API endpoint before replacing UNKNOWN in seed_row.json, then commit only tools/uniswap-v4-upgrade-watch/. Nothing was published externally.
