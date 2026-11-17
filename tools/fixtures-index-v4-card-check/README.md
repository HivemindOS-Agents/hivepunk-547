---
license: mit
language: en
tags:
- fixtures
- inventory
---

# fixtures-index-v4

Sample dataset card for the fixtures-index-v4 inventory, and the guide
for the card-check tool in this folder. The card below is what
`card_check.py` validates: frontmatter, dataset name, and file list.

## Files

- inventory.py
- self_test.py
- README.md
- INVENTORY.md

## How to run

From this folder:

~~~bash
# Validate the included sample card (README.md) against data.csv:
python3 card_check.py

# Validate other files:
python3 card_check.py /path/to/README.md /path/to/data.csv fixtures-index-v4

# Self-test (no arguments, no network):
python3 self_test.py
~~~

What it checks: frontmatter has non-empty `license`, `language`, and
`tags`; the dataset name `fixtures-index-v4` appears as the exact
`# fixtures-index-v4` heading; and the Files list above matches the
`file_name` values in `data.csv` exactly (no missing, extra, or
duplicate names). It only reads files as data, uses no network, and
publishes nothing.

## Untested

- Frontmatter parsing is a small YAML subset (scalar keys, `tags` as
  inline list or `-` items); quoted, nested, or multi-line YAML, and
  other Hugging Face card fields, are not parsed or validated here.
- `license` and `language` values are checked only for non-emptiness;
  they were not checked against a live Hugging Face allow-list.
- Links and URLs in the card were not fetched; this step could not
  confirm any live dataset page.
- `SELFTEST_OUTPUT.md` in this folder, if present later, is written by
  the HivemindOS runner after the commit; this tool never writes it,
  and no output or pass line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
