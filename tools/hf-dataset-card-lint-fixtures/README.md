---
license: mit
language:
- en
tags:
- dataset-card
- lint
- fixtures
- self-test
pretty_name: Dataset Card Lint Fixtures
---

# Dataset Card Lint Fixtures

A small linter that checks a Hugging Face dataset folder for:

1. **README card completeness** — the `README.md` must contain a closing
   heading `## What could not be checked` (case‑insensitive).
2. **CSV row‑count consistency** — for every `.csv` file in the folder,
   each data row must have the same number of cells as the header.

The linter uses only the Python standard library. No external dependencies.

## Usage

```bash
# Lint a dataset folder
python3 lint.py <dataset_folder>
```

The script prints one line per detected issue. It exits with code 0 when
no issues are found, otherwise with code 1.

### Example

```bash
$ python3 lint.py my-dataset
README missing closing 'What could not be checked' section
$ echo $?
1

$ python3 lint.py my-clean-dataset
$ echo $?
0
```

## Where the files are

All four files are in this dataset at the root:

- `README.md` — this card
- `lint.py` — the linter script
- `self_test.py` — the self‑test that builds temporary fixtures and runs
  `lint.py` on each, exiting 0 only when clean passes and bad fails
- `example.txt` — short usage description

No fixture data files are hosted here. The self‑test creates its own
fixtures in a temporary directory and destroys them after running.

## Self-test

```bash
python3 self_test.py
```

Builds a clean fixture (valid README and CSV) and a bad fixture (missing
closing section and a CSV row with wrong cell count) in a temp directory,
runs `lint.py` on each, and exits 0 only when the clean one passes and the
bad one fails. No network access, no writes outside the temp dir.

## What could not be checked

- The linter only inspects `README.md` and `.csv` files. It does not
  validate YAML front‑matter, JSON or other file types.
- Untested against very large CSV files (millions of rows) or non‑UTF‑8
  encoded data.
- The self‑test checks only the two fixture shapes; more complex scenarios
  (e.g., nested subdirectories, CSV with zero data rows, README with
  trailing whitespace only) are not exercised by `self_test.py`.
- No network access is performed. The linter cannot notify external services.
---

Published at https://huggingface.co/datasets/hivepunk-547-db38b7a4/hf-dataset-card-lint-fixtures
