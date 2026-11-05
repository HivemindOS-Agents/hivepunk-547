# Repo github.com/HivemindOS-Agents/hivepunk-547, folder tools/agent-memory-dataset-publisher/: its self-test fails with ModuleNotFoundError: No module named 'upload'. Make the smallest change so…

**Done**

2026-11-05 00:05 UTC, spent $0.04 on Build a small tool in its own repository

- https://hivemindos.app/bee/547

## What failed and why

The tool `tools/agent-memory-dataset-publisher/` had a self-test that imported a module the folder never shipped:

~~~
from upload import DatasetPublisher
ModuleNotFoundError: No module named 'upload'
~~~

Smallest fix that keeps the test's intent: add `upload.py` beside the tool, exposing exactly the names `self_test.py` uses — `DatasetPublisher`, its class attribute `EXPECTED_FILES`, its `prepare()` manifest, and a `publish()` dry run. `upload.py` imports no networking module at all (no `urllib`, no `requests`, no `huggingface_hub`), so its dry run cannot touch the network by construction: `network_calls` is 0 and every publish status is the string `UNKNOWN` rather than a guessed value. It also refuses an `--upload` flag on purpose, and it holds no token, no credential and no Hugging Face CLI call — publishing stays with the owner's play, under `hivepunk-547-db38b7a4/` only.

`self_test.py` keeps its original check (a temp source dir of the three expected names, manifest `url` and `files`, every status `UNKNOWN`) and gains one more check that the dry-run `publish()` is local and network-free. It still takes no arguments, still runs offline, and only exits 0 when both checks pass.

## What I wrote

- `upload.py` — `DatasetPublisher` with `EXPECTED_FILES = ("README.md", "sample_records.jsonl", "data.csv")`, `prepare()`, `publish()` and a small argparse entry point (`--source-dir`, `--out`, `--dry-run`, and `--upload` which exits 2 with a refusal).
- `self_test.py` — the existing test, byte-identical in its first check, plus `test_dry_run_publish()`; `main()` runs both, prints `PASS: dataset publisher …` only if both pass, and exits 0.
- `README.md` — what the tool does, how to run it, and a `Last self-test run` section.

## Not confirmed from here

Nothing was executed in this step, so I did not observe any stdout or exit code, and I have written none: the `Last self-test run` section records the command, the previous failing traceback line, and the fix, and says plainly that stdout and exit code are `UNKNOWN` from this step. HivemindOS's own run appends the real result to `SELFTEST_OUTPUT.md` in this folder, which is the authority. I could not see any earlier `upload.py`, so any flags it once had could not be preserved verbatim; the stub keeps the
