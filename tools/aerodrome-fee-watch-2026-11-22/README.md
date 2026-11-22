# aerodrome-fee-watch-2026-11-22

opportunity: none

## Caveats first

- Labels are hand-derived from research/2026-11-22-aerodrome-finance.md as summarised in history, not source-verified by re-fetch in this writing step.
- Only the research note's summary and source list were available in this step; no new figures are added.
- Could not confirm: live fee tiers, pool liquidity, TVL, volume, emissions, merger status, source-page wording, or self-test exit 0.
- Do not touch tools/agent-memory-lint-fixtures/ for this work. Nothing here was published externally.

## What this is

Dated Aerodrome Finance fee/liquidity watch report (2026-11-22-aerodrome-fee-watch.md), based on research/2026-11-22-aerodrome-finance.md, with FACT/DERIVED/UNKNOWN labels and source links.

## How to use

~~~bash
python3 self_test.py
~~~

Run self_test.py with no arguments, no network, alone from this folder. It checks the report, this README and ARTIFACTS.md for the date, all three labels, exact FACT 5 / DERIVED 2 / UNKNOWN 3 table counts, all five source URLs, the research-note link, caveats and untested marks, and exits 0 only when every check passes.

## Untested parts (marked untested)

- UNTESTED: source pages were not re-fetched; FACT claims may no longer be on their pages.
- UNTESTED: no on-chain query was run; no live fee, liquidity, TVL or volume figure is stated.
- UNTESTED: full research-note text was not in the tools listing; report stays at history-summary level.
- UNTESTED: Velodrome merger status/terms not checked; listed as UNKNOWN.
- UNTESTED: self-test exit 0 not confirmed from this writing step; HivemindOS runner result in SELFTEST_OUTPUT.md is authoritative.

## ARTIFACTS.md log

See ARTIFACTS.md in this folder for the artifact list, exact command, raw-output slot and commit note.

Made by HivePunk #547, an AI agent on HivemindOS. A person decides; an agent never merges or publishes.
