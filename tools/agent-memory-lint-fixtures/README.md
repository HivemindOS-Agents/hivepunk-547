# agent-memory-lint-fixtures

A small fixture set plus a rule-checker for memory-record label discipline: **a record whose hand labels disagree with the computed labels must carry a note; a record that agrees must not.**

## Files

- `sample_records.jsonl` — six records, ids `L004`, `L005`, `L012`, `L013`, `L018`, `L020`. Ids and every field other than `note` are unchanged. No key, password, personal detail or private value appears in any record.
- `lint_records.py` — the checker. Rule (unchanged): a record whose `expected_labels` disagree with the computed labels MUST carry a `note`; a record that agrees MUST NOT. Computed labels: `body` (empty / nonempty), `origin` (sourced / unsourced), `date` (stale / fresh — more than 365 days before the fixed reference date `2026-11-01`). It reads files, writes nothing, and imports only `argparse`, `datetime`, `json`, `sys`, `pathlib` — no networking library appears in it.
- `self_test.py` — runs with no arguments and no network: it imports the checker beside it, runs it over this sample plus a synthetic pre-fix copy built in a temp folder, and exits 0 only when all eight checks pass. Checks: rule constants unchanged; the sample has exactly those six ids in that order with only the known fields; linting the sample gives zero violations; the checker itself derives exactly the four disagreeing and two agreeing ids and the four notes quote their computed labels; rebuilding the pre-fix state yields exactly the six expected messages, wording included; label branches tested directly, including the 365/366-day boundary and an unparseable date; CLI exit 0 on the sample from a different working directory and exit 1 with six lines on the pre-fix copy; and the checker's source text names no networking or credential symbol.
- `README.md` — this file.

## What it does

Given a source folder that should hold exactly these three files:

1. `README.md`
2. `sample_records.jsonl`
3. `data.csv`

it builds a manifest (URL, expected file names, which are present, which are missing, sizes) and offers a **local dry run** of the publish step. Every file status is the string `UNKNOWN`: the tool never guesses a result it did not observe.

The module imports only `argparse`, `json`, `sys` and `pathlib` — no networking library appears in it at all, so the dry run has no code path to the network. It holds no key, reads no credential, and runs no uploader command. `network_calls` is `0` and `credentials_read` is `false` in every result.

## How to run it

### Library use

```python
from upload import DatasetPublisher, prepare, publish

manifest = prepare("/path/to/source")          # URL, files (all UNKNOWN), missing
result = publish("/path/to/source")            # local dry run, network_calls 0
refused = publish("/path/to/source", upload=True)  # status REFUSED, no request

publisher = DatasetPublisher("/path/to/source")
publisher.present_files(), publisher.missing_files()
```

### Command line (dry run, prints JSON)

```bash
python3 upload.py --source-dir /path/to/source
python3 upload.py --source-dir /path/to/source --dry-run
python3 upload.py --source-dir /path/to/source --out published.json
```

`--upload` is refused on purpose: it prints a `REFUSED:` line and exits **2**.

### Self-test (no arguments, no network)

```bash
python3 self_test.py
```

It puts its own folder on `sys.path` first, so it works from any working
directory, uses temporary folders only, and exits 0 only when all nine checks
pass.

## Untested

- **The post‑fix run of `self_test.py` has not been observed** from where this was written. No interpreter was run for this change, so no exit code or stdout is claimed here.
- Any CLI path against a real dataset folder outside temporary directories.
- Files that exist but are empty, unreadable, or symlinks: only presence and size are looked at, never content.
- Anything about the live dataset: no HTTP request, no page read, no Dataset Viewer field read, and no upload occurred.
- Whether the published repo's file names still match the three expected names.
- No earlier version of `upload.py` was visible, so no older flags could be kept verbatim; only the imported names are matched exactly.

## Self-test

Result: UNKNOWN — not yet read
