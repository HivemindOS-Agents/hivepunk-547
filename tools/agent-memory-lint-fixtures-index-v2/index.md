# agent-memory-lint-fixtures-index-v2 — fixture index

One row per fixture path under the recorded `fixtures_root`
(`tools/agent-memory-lint-fixtures/`). The same three rows, in the same order,
are in `index.json`; `self_test.py` reads both files and checks them against
each other, so any edit here must be made in `index.json` too.

| path | rule | description | expected_exit_code |
|---|---|---|---|
| `clean/` | no findings on a clean fixture | lint over this fixture produces no findings and exits 0 | 0 |
| `bad-rows/` | row count or empty-cell finding | lint over this fixture reports a row-count or empty-cell finding and exits 1 | 1 |
| `bad-card/` | missing closing 'What could not be checked' section | lint over this fixture reports a card missing its closing 'What could not be checked' section and exits 1 | 1 |

The exit codes are the ones a memory-lint run over each fixture is meant to
return; they are recorded intent, not a measurement made in this folder.
