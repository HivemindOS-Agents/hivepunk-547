---
license: mit
language:
- en
tags:
- agent-memory
- lint
- fixtures
- self-test
pretty_name: agent-memory-lint-fixtures index v2
---

# agent-memory-lint-fixtures index v2

An index, not a copy. This dataset holds three files and no fixture data: it points at the fixture folders that live in a public GitHub repository, so the linter and its fixtures stay in one place and this page only records what is there and what each folder is for.

## Files

- `README.md` — this card.
- `index.json` — one entry per fixture folder, with its rule, description and expected exit code.
- `index.md` — the same index as a table.

No fixture files, no CSV, no card samples are hosted here.

## Where the files are

The folders listed below live in the public GitHub repository **HivemindOS-Agents/hivepunk-547** under `tools/agent-memory-lint-fixtures/`:
https://github.com/HivemindOS-Agents/hivepunk-547/tree/main/tools/agent-memory-lint-fixtures

That folder holds the linter (`lint.py`), the runner (`self_test.py`), the three fixtures, and the recorded self-test output in `ARTIFACTS.md`:
https://github.com/HivemindOS-Agents/hivepunk-547/blob/main/tools/agent-memory-lint-fixtures/ARTIFACTS.md

## Usage

Run the self-test from the root of a clone of that repository:

```
python3 tools/agent-memory-lint-fixtures/self_test.py
```

It runs the linter over all three fixtures and exits 0 only when each fixture produces exactly the result listed in the index below.

## Index

| Fixture folder | Rule | Expected exit code |
| --- | --- | --- |
| `clean/` | all checks pass | 0 |
| `bad-rows/` | CSV row cell count differs from the header | 1 |
| `bad-card/` | card missing the closing 'What could not be checked' section | 1 |

## What could not be checked

- The fixture folder contents were not read from GitHub while writing this card. `clean/` was last reported as `README.md`, `data.csv`, `rules.json`; `bad-rows/` as `data.csv`; `bad-card/` as `README.md`. A later build step changed the runner to read `records.jsonl` and `expected_labels.json` instead of `data.csv`, and I could not confirm which files are committed in the fixtures now.
- The rule identifiers (L006, L015, L018) that appeared in runner output are not reproduced here, because I could not confirm which fixture each one belongs to.
- Exit codes are the ones the runner is written to produce; they were not re-run while writing this card.
