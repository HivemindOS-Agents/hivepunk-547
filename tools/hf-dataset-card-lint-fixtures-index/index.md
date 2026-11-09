# Fixture index

Same three entries as `index.json`.

| Fixture folder | Rule | Description | Expected exit code |
| --- | --- | --- | --- |
| `clean/` | all checks pass | Well-formed fixture: card has its closing section, every CSV row matches the header cell count. | 0 |
| `bad-rows/` | CSV row cell count differs from the header | One deliberately spaced row; the linter must name the row and both counts. | 1 |
| `bad-card/` | card missing the closing 'What could not be checked' section | README with no closing section; the linter must flag it by name. | 1 |

All three folders live under `tools/agent-memory-lint-fixtures/` in github.com/HivemindOS-Agents/hivepunk-547. No fixture files are hosted in this dataset.
