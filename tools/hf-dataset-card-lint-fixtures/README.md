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

A small linter that checks a dataset folder for two things:

1. **README card completeness** — the `README.md` must carry a closing
   heading `## What could not be checked` (case-insensitive).
2. **CSV row-count consistency** — for every `.csv` file in the folder,
   each data row must have the same number of cells as its header.

The linter uses only the Python standard library. No external dependencies
and no network access.

## Files in this dataset

Four files, all at the root of the dataset, and no others:

- `README.md`
- `lint.py`
- `self_test.py`
- `example.txt`

Read-back after upload:

    GET https://huggingface.co/datasets/hivepunk-547-db38b7a4/hf-dataset-card-lint-fixtures -> status ___
    Listed files: ___, ___, ___, ___

No fixture data files are hosted. `self_test.py` builds its own fixtures in
a temporary directory and removes them afterwards.

## Usage

~~~bash
python3 lint.py <dataset_folder>
~~~

The script prints one line per detected issue. It exits 0 when no issues
are found, otherwise 1.

### Example

~~~bash
$ python3 lint.py my-dataset
README missing closing 'What could not be checked' section
$ echo $?
1

$ python3 lint.py my-clean-dataset
$ echo $?
0
~~~

## Self-test

~~~bash
python3 self_test.py
~~~

Builds a clean fixture (valid card and CSV) and a bad fixture (missing
closing section and a CSV row with the wrong cell count) in a temp
directory, runs `lint.py` on each, and exits 0 only when the clean one
passes and the bad one fails. No arguments, no network, and no writes
outside the temp directory.

## What could not be checked

- The four filenames listed above were not compared against the live file
  listing of the dataset page by the step that wrote this card.
- The linter only inspects `README.md` and `.csv` files. It does not
  validate YAML front-matter, JSON, or other file types.
- Untested against very large CSV files or non-UTF-8 encoded data.
- `self_test.py` exercises only the two fixture shapes; nested
  subdirectories, a CSV with zero data rows, and a README holding only
  whitespace are not exercised.
- No network access is performed by the linter or the self-test.

Dataset page:
https://huggingface.co/datasets/hivepunk-547-db38b7a4/hf-dataset-card-lint-fixtures
