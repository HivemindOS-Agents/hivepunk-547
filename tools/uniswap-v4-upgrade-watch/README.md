# uniswap-v4-upgrade-watch

## Caveats first

- Could not confirm: latest release tag/date for Uniswap/v4-core from https://github.com/Uniswap/v4-core/releases in this step. They are UNKNOWN in seed_row.json.
- The v4.0.0 / 2025-01-23 claim is unverified and kept separate; it is not the verified latest release.
- UNTESTED: live GitHub releases page, live repository state, and self-test exit 0 from this writing step. HivemindOS runner result in SELFTEST_OUTPUT.md is authoritative.
- Do not touch tools/agent-memory-lint-fixtures/ for this work. Nothing here was published externally. A person decides; an agent never merges or publishes.

## What this is

Seed row for a Uniswap v4 upgrade watch. seed_row.json records Uniswap/v4-core with latest_release_tag and latest_release_date as UNKNOWN unless verified from https://github.com/Uniswap/v4-core/releases, with source URLs and the unverified v4.0.0/2025-01-23 claim kept separate.

## How to use

~~~bash
python3 self_test.py
~~~

Run with no arguments, no network, alone from inside this folder. It checks seed_row.json is valid JSON, verified fields are UNKNOWN, unverified claim is separate, source URLs are present, and README/ARTIFACTS carry caveats and untested marks. Exits 0 only when every check passes.

To verify: open https://github.com/Uniswap/v4-core/releases, read the latest release tag and date verbatim, then update only the verified fields in seed_row.json and the verification output slot in ARTIFACTS.md.

## Untested parts (marked untested)

- UNTESTED: latest release tag/date not verified from the live releases page; seed_row.json keeps UNKNOWN.
- UNTESTED: v4.0.0 / 2025-01-23 claim not verified against the releases page.
- UNTESTED: self-test exit 0 not confirmed from this writing step; runner result is authoritative.
- UNTESTED: no live GitHub fetch was made in this writing step.

## ARTIFACTS.md log

See ARTIFACTS.md in this folder for artifact list, exact command, verification output slot, and commit note.

Made by HivePunk #547, an AI agent on HivemindOS. A person decides; an agent never merges or publishes.
