# uniswap-v4-upgrade-watch

## Caveats first

- Could not confirm: latest release tag/date for Uniswap/v4-core from https://api.github.com/repos/Uniswap/v4-core/releases/latest in this step. They are UNKNOWN in seed_row.json; no tag or date was invented.
- The v4.0.0 / 2025-01-23 claim is unverified and kept separate; it is not the verified latest release.
- UNTESTED: live GitHub API verification. Self-test exit 0 in ARTIFACTS.md is from the latest HivemindOS runner run 45347241694 (2026-11-24 07:21 UTC); a re-run after this update is UNTESTED from this writing step and the runner's new SELFTEST_OUTPUT.md is authoritative.
- Do not touch tools/agent-memory-lint-fixtures/ for this work. Nothing here was published externally. A person decides; an agent never merges or publishes.

## What this is

Seed row for a Uniswap v4 upgrade watch. seed_row.json records Uniswap/v4-core with latest_release_tag and latest_release_date as UNKNOWN unless verified from https://api.github.com/repos/Uniswap/v4-core/releases/latest, with source URLs and the unverified v4.0.0/2025-01-23 claim kept separate.

## How to use

~~~bash
python3 self_test.py
~~~

Run with no arguments, no network, alone from inside this folder. It checks seed_row.json is valid JSON, verified fields are UNKNOWN, the API source_url is present, the unverified claim is separate, and README/ARTIFACTS carry caveats and untested marks. Exits 0 only when every check passes.

To verify: fetch https://api.github.com/repos/Uniswap/v4-core/releases/latest, read tag_name and published_at verbatim, then update only the verified fields in seed_row.json.

## Untested parts (marked untested)

- UNTESTED: latest release tag/date not verified from the live GitHub API; seed_row.json keeps UNKNOWN.
- UNTESTED: v4.0.0 / 2025-01-23 claim not verified against the API.
- UNTESTED: re-run of self_test.py after this update not confirmed from this writing step; runner exit 0 for run 45347241694 is pasted in ARTIFACTS.md and the new runner result is authoritative.
- UNTESTED: no live network fetch was made in this writing step.

## ARTIFACTS.md log

See ARTIFACTS.md in this folder for artifact list, exact command, raw exit-0 output, and commit note.

Made by HivePunk #547, an AI agent on HivemindOS. A person decides; an agent never merges or publishes.
