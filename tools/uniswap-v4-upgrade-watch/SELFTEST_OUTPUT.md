# Self-test of uniswap-v4-upgrade-watch

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-25T20:27:53Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45695133520
- Tested commit: cd847d8871f3cd3d8fec5b5124e36a466a3f99f7
- Verified by: none
- Check from: none

What it printed (what failed first, then its last lines):

~~~
FAIL: verify_upload.py must not contain upload code
watch.load_seed(data/seed_row.json): v4.0.0/2025-01-23T19:00:03Z release_id 196495150
watch: v4.0.0/2025-01-23T19:00:03Z release_id 196495150 prerelease=False draft=False source=https://api.github.com/repos/Uniswap/v4-core/releases/latest
hf_manifest.build_manifest(): upload README.md, data/seed_row.json with matching sha256
~~~
