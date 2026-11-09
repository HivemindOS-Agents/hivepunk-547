~~~markdown
# Agent‑Memory‑Lint‑Fixtures

This repository contains a tiny linter (`lint.py`) that checks two aspects of a Hugging Face
dataset folder:

1. **CSV row‑count consistency** – for every CSV file in the folder, the linter reports any row whose
   cell count differs from the header.
2. **README closing section** – the README.md must end with a heading titled
   `## What could not be checked`.

The linter is intentionally minimal; it has no external dependencies apart from the
standard library.

## How to run

```bash
# Lint a single fixture folder
python3 lint.py <folder>
```

The script prints one line per detected issue. It exits with code `0` if no issues are
found, otherwise with `1`.

## Self‑test

```bash
python3 self_test.py
```

`self_test.py` runs the linter against the three supplied fixture folders and records the
output in `ARTIFACTS.md`. It exits `0` only when all expected results match.

## What could not be checked

- The linter only inspects files present in the supplied folder; it assumes the directory
  structure follows the handful of fixtures in this repository. It does not recursively
  search external directories or mount network drives.
- The linter is untested against very large CSV files or non‑utf‑8‑encoded data.
- No network access is performed by the linter or the self‑test.

---

Learn more about dataset card formatting at
https://huggingface.co/docs/hub/en/datasets-cards.
~~~
