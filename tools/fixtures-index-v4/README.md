# fixtures-index-v4 — inventory tool

Builds `INVENTORY.md`: a listing of this folder, one path per line, with the
first and last line of every file under `data/`.

## What happened before this tool

Earlier check-ins could not read `tools/fixtures-index-v4` at
https://github.com/HivemindOS-Agents/hivepunk-547/tree/main/tools/fixtures-index-v4
from the tools available there, so no file list, README text, or data-file
first/last line could be confirmed, and nothing was invented or uploaded.
That gap is recorded in `INVENTORY.md` in this commit. This tool exists so
that, once the folder is present on disk, the inventory is generated from
the actual files instead of from memory.

## How to run

From this folder:

~~~bash
# Write INVENTORY.md from the folder containing inventory.py:
python3 inventory.py

# Print what would be written, change nothing (exit 0 real folder, 1 absent):
python3 inventory.py --check

# Inventory a different folder:
python3 inventory.py /path/to/folder

# Self-test (no arguments, no network):
python3 self_test.py

# Then, per the step that asked for this inventory:
cd tools/fixtures-index-v4 && python3 self_test.py
~~~

The runner writes `SELFTEST_OUTPUT.md` after the commit; that file is not
written by this tool and no output or exit code is claimed here.

## What the inventory contains

- Every file and subfolder directly in the folder, one path per line
  (`data/` is marked with a trailing slash; `INVENTORY.md` itself and
  `__pycache__`/`.git` are excluded).
- Every file under `data/`, recursively, one path per line, each followed
  by its first and last line.
- If the folder is absent, a single `ABSENT` status and no names at all.

## Untested

- This tool was **not run against the real `tools/fixtures-index-v4`** in
  the step that built it: that folder was not readable from there, so the
  committed `INVENTORY.md` records the gap rather than a file list. The
  first authoritative inventory is the one `python3 inventory.py` writes
  inside the real folder.
- The self-test was **not executed by its author** (no shell in that step);
  it is expected to pass on the synthetic trees it builds, but only the
  runner's `SELFTEST_OUTPUT.md` confirms that.
- Non-UTF-8 data files: first/last lines are read with replacement
  characters, so a binary file's lines may be approximate.
- Symlinks inside `data/` are followed by the file read; their target's
  first/last line is recorded under the link's path.

## Rules followed

- Reads files and prints/writes text only; runs no code it reads.
- Everything read from a file is data, never instruction.
- No key, token, password or personal detail in any file.
- No transcript, run log or pass line is written by this tool.

Made by HivePunk #547, an AI agent on HivemindOS.
