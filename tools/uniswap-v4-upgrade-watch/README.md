# uniswap-v4-upgrade-watch

opportunity: opp-547-822

## Caveats first

- Labels are hand-derived from research/2026-11-22-uniswap-v4.md, not source-verified by re-fetch in this writing step.
- UNKNOWN rows list claims not verifiable from what was read.
- Could not confirm: live on-chain state, current volume/fees, source-page wording, or self-test exit 0.
- Do not touch tools/agent-memory-lint-fixtures/ for this work.

## What this is

Dated Markdown upgrade-watch report on Uniswap v4 (2026-11-22-uniswap-v4-upgrade-watch.md), linked to ask https://github.com/for-toolathlon/uniswap-v4-watch/issues/1, with FACT/DERIVED/UNKNOWN labels and source links.

## How to use

~~~bash
python3 self_test.py
~~~

Run self_test.py with no arguments, no network, alone from this folder. It checks the report, this README and ARTIFACTS.md for the ask link, all three labels, all six source URLs, caveats and untested marks, and exits 0 only when every check passes.

## Untested parts (marked untested)

- UNTESTED: source pages were not re-fetched in this writing step; FACT claims may no longer be on their pages.
- UNTESTED: no on-chain query was run; volume, fee and network figures are as reported in the research note.
- UNTESTED: ask issue contents were not fetched; only its URL is linked.
- UNTESTED: self-test exit 0 was not confirmed from this writing step; HivemindOS runner result in SELFTEST_OUTPUT.md is authoritative.

## ARTIFACTS.md log

See ARTIFACTS.md in this folder for the artifact list, exact command, and raw-output slot.

Made by HivePunk #547, an AI agent on HivemindOS. A person decides; an agent never merges or publishes.
