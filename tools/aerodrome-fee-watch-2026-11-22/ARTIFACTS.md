# aerodrome-fee-watch-2026-11-22: artifact record

## Artifacts

- 2026-11-22-aerodrome-fee-watch.md - dated fee/liquidity watch, FACT 5 / DERIVED 2 / UNKNOWN 3, based on research/2026-11-22-aerodrome-finance.md, five source links.
- README.md - caveat-first usage and untested limits.
- self_test.py - standalone checks, no args, no network.
- ARTIFACTS.md (this file) - this record and commit note.

## Exact command

~~~bash
python3 self_test.py
~~~

Run from inside this folder: tools/aerodrome-fee-watch-2026-11-22/

## Raw output slot

~~~text
(paste the runner's raw SELFTEST_OUTPUT.md text here, unedited; nothing here is a run log)
~~~

## What was confirmed, and what was not

- NOT confirmed: that python3 self_test.py exits 0. No run seen from this writing step. SELFTEST_OUTPUT.md by runner is authoritative.
- NOT confirmed: live source pages, on-chain fee/liquidity state, merger status, or full research-note wording beyond history summary.
- Confirmed by reading this folder only: report/README/this file contain date, FACT/DERIVED/UNKNOWN labels, five source URLs, research-note link, and untested marks checked by self_test.py.

## Commit note (for agents-service commit to this repo only)

Title: Built aerodrome-fee-watch-2026-11-22 dated fee/liquidity watch with README, ARTIFACTS and self-test
What: report based on research/2026-11-22-aerodrome-finance.md, FACT 5/DERIVED 2/UNKNOWN 3, five sources; README; ARTIFACTS; self_test.
Spent: writing step only; no network calls, no external publish.
Links: research note https://github.com/HivemindOS-Agents/hivepunk-547/blob/main/research/2026-11-22-aerodrome-finance.md and sources in report.
Unchecked: source re-fetch, live fee/liquidity figures, merger status, self-test runner result.

## Left for owner

Owner: let runner run python3 self_test.py alone in this folder, paste raw output into slot, then commit/publish separately if wanted.
