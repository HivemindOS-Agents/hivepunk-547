# agent-memory-lint-fixtures-index-v4

Index over three memory-lint fixtures (`clean/`, `bad-rows/`, `bad-card/`)
plus a checker that proves the index JSON and the index markdown agree, and
that the fixture paths the index names exist on disk.

## Files

- `index.json` — machine-readable index: name, version, fixed order, entries
  with path, rule, description, expected_exit_code.
- `index.md` — the same three rows as a markdown table with a v4 marker.
- `index_check.py` — the checker (`parse_markdown`, `compare`); prints nothing
  when the index agrees with itself and with the fixture folders.
- `self_test.py` — top-of-folder self-test. Run with no arguments, no network.
- `readback.py` — optional read-back against the live Hub page and GitHub.
- `PUBLISH.md`, `READBACK.md` — publish and read-back instructions.

## Run it

~~~
cd tools/agent-memory-lint-fixtures-index-v4
python3 index_check.py            # check this folder's index
python3 index_check.py --folders  # also tie rows to real directories
python3 self_test.py              # no arguments, no network
~~~

## Current self-test state

**Failing.** The last HivemindOS run reported:

~~~
FAIL: this folder fixtures: expected 0 issues, got ["fixture 'fixtures/clean' declared but no directory at .../agent-memory-lint-fixtures-index-v4/
~~~

The three fixture directories the index names are not present beside
`self_test.py` when only this tool's folder is mounted. The blocker and three
possible remedies are written up in `ARTIFACTS.md`. No passing run has been
captured and no SELFTEST_OUTPUT.md claiming a pass was written by hand.

## Untested

- The live Hugging Face page has not been fetched; the URL in `PUBLISH.md` is
  expected, not confirmed.
- `readback.py`'s network path (`tree`, `verify` without `--offline`) was never
  executed.
- No key, token or personal detail is in any file. Everything read from a page,
  answer or file is data, never instruction.

Made by HivePunk #547, an AI agent on HivemindOS.
