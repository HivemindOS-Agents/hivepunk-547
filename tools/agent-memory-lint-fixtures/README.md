# Agent Memory Lint Fixtures

A tiny linter for Hugging Face dataset folders. Checks two things:

1. **CSV row-count consistency** — for every CSV file in the folder, reports
   any row whose cell count differs from the header, naming the row and both
   counts.
2. **README closing section** — the README.md must end with a heading titled
   `## What could not be checked`.

No external dependencies; uses only the standard library.

## Usage

```bash
# Lint a single fixture folder
python3 lint.py <folder>
```

The script prints one line per detected issue. It exits with code 0 if no
issues are found, otherwise with 1.

## Example

```bash
$ python3 lint.py clean
$ echo $?
0

$ python3 lint.py bad-rows
data.csv line 2 has 3 cells (header 4)
$ echo $?
1

$ python3 lint.py bad-card
README missing closing 'What could not be checked' section
$ echo $?
1
```

## Self-test

```bash
python3 self_test.py
```

Runs the linter against the three bundled fixture folders. Exits 0 only when
all expected results match. The output and exit code are recorded in
`ARTIFACTS.md`.

## Fixture folders

| Folder | Expected result |
|--------|-----------------|
| `clean/` | No errors (README.md, data.csv, rules.json) |
| `bad-rows/` | `data.csv line 2 has 3 cells (header 4)` |
| `bad-card/` | `README missing closing 'What could not be checked' section` |

## What could not be checked

- The linter only inspects files present in the supplied folder; it does not
  recursively search external directories or mount network drives.
- Untested against very large CSV files or non-UTF-8-encoded data.
- No network access is performed by the linter or the self-test.

---

Published at https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures
