# GOAL: uniswap-v4-upgrade-watch

Track the latest Uniswap/v4-core release from https://api.github.com/repos/Uniswap/v4-core/releases/latest, recording tag_name and published_at verbatim in seed_row.json only if verified, else UNKNOWN, never invented. Current verified row: v4.0.0 / 2025-01-23T19:00:03Z, release id 196495150.

Success: python3 self_test.py run alone offline in this folder exits 0, README marks untested parts, and ARTIFACTS.md carries the raw exit-0 output in the same commit.

Could not confirm: whether v4.0.0 is still the latest release at read time.
