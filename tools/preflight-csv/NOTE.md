# NOTE.md — Files written for preflight-csv

## Files in this folder (`tools/preflight-csv/`)

| File | Description | Status |
|---|---|---|
| `preflight_csv.py` | Main script; Python 3, stdlib only. | UNTESTED (see self_test.py) |
| `README.md` | Usage and documentation. | Tested-text (written, not verified on a real terminal) |
| `sample.csv` | Example CSV for quick validation. | Included as-is |
| `self_test.py` | Automated test: runs the tool on known-good and known-bad inputs, checks output. | UNTESTED (run it with `python3 self_test.py`) |

## What has not been tested

- The script has not been executed against any real file in this environment.
- The sample file has not been opened by any CSV viewer.
- No network access was used; no external data was fetched.

## Left for the owner

1. Run `python3 self_test.py` to verify that the script works on the test cases.
2. Run the script on a real CSV file of your choice to confirm expected behaviour.
3. If any improvements are needed, edit the files here and re-run the tests.

---

*Written by HivePunk 547 on 2026-10-30 as part of a preflight-check packaging task.*
