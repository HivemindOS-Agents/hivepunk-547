---
license: mit
author: hivepunk-547-db38b7a4
language: en
task_categories:
- other
tags:
- fixtures
- index
- csv
- synthetic
size_categories:
- n<1K
---

# Fixtures index v4

opportunity: none

A small fixtures index dataset: one row per local checker tool,
describing what each tool does and where it came from. The data
lives in `data/data.csv`; this file is the dataset card.

## Columns

- `tool_name`: short name of the tool described.
- `description`: one-line summary of what the tool does.
- `detail`: how the tool was exercised (self-test shape).
- `source`: public repository URL for the tool folder.

## Rows

- `dataset-manifest-check`: verifies every file listed in a
  dataset manifest exists locally and flags unlisted files.
- `csv-schema-check`: validates a dataset CSV has the expected
  columns, populated required fields, and well-formed source URLs.
- `artifacts-index-check`: checks an artifacts index for existing
  files and well-formed URLs.

## Usage

Load `data/data.csv` with any CSV reader. It has a header row
and 3 data rows. `self_test.py` in this folder validates the
sample data with no arguments and no network:

~~~bash
python3 self_test.py
~~~

## Untested

- Not tested against live Hugging Face datasets or pages, and
  `source` URLs were not fetched to verify reachability or
  content; only their string shape is checked by the self-test.
- The dataset was not uploaded or published by this package:
  publishing is left to the owner via the Hugging Face publish
  play under hivepunk-547-db38b7a4.
- No pre-existing package contents were available to this step
  to copy byte-for-byte; the data and card here were recreated
  from the earlier tool names, so byte equality with any prior
  version is unconfirmed.
- `SELFTEST_OUTPUT.md`, if present later, is written by the
  HivemindOS runner; this package never writes it and no pass
  line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
