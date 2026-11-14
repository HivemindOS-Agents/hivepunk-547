# Index — agent-memory-lint-fixtures v4

Version marker: **v4**. Three fixture rows below. A table without the v4 marker
is not this file.

| Path | Rule | Expected exit code |
|---|---|---|
| `fixtures/clean/` | no findings on a clean fixture | 0 |
| `fixtures/bad-rows/` | row count or empty-cell finding | 1 |
| `fixtures/bad-card/` | missing closing 'What could not be checked' section | 1 |

Every row above has an entry in `index.json` with the same `path`, `rule` and
`expected_exit_code`. `index_check.py` asserts that and prints nothing if it
holds.

Fixture folders ship as `fixtures/clean/`, `fixtures/bad-rows/` and
`fixtures/bad-card/`; the `--folders` mode of the checker is what ties these
rows to real directories.
