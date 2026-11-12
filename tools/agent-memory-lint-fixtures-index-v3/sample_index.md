# sample index — agent-memory-lint-fixtures-index-v3

A clean, self-contained index pair. The three rows below match
`sample_index.json` exactly (same paths, same order, same rule, description
and `expected_exit_code`), so `index_check.analyze()` finds nothing to report
and `self_test.py`'s "clean sample" case passes.

The path cell must be wrapped in backticks; the table must have four columns
and a trailing pipe on every row, which is what `index_check.py` matches.

| path | rule | description | expected_exit_code |
|---|---|---|---|
| `clean/` | no findings on a clean fixture | lint over this fixture produces no findings and exits 0 | 0 |
| `bad-rows/` | row count or empty-cell finding | lint over this fixture reports a row-count or empty-cell finding and exits 1 | 1 |
| `bad-card/` | missing closing 'What could not be checked' section | lint over this fixture reports a card missing its closing section and exits 1 | 1 |

The exit codes are recorded intent (what a memory-lint run over each fixture is
meant to return), not a measurement made in this folder.
