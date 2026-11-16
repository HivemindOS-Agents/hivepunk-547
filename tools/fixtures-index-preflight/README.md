# fixtures-index-preflight

An offline preflight for publishing a tool folder as a Hugging Face dataset:
list what would go up, and check the page's file list against it. It exists
because a publish step that reads a folder it cannot see must stop rather than
compose a substitute card.

## What it does

- `preflight.py list SOURCE_DIR [--json OUT]` prints one path per line for
every file and subfolder directly in the folder plus everything under `data/`,
and writes a manifest (path, bytes, sha256) when `--json` is given. It skips
`SELFTEST_OUTPUT.md`, `.git`, `__pycache__`/`.pyc`, `.DS_Store`,
`.ipynb_checkpoints`, `.pytest_cache` and symlinks, each with a stated reason.
- A missing folder, or one with no top-level `README.md`, prints `STOP: ...`
and exits 1. The publish must not proceed; no substitute `README.md` is made.
- `preflight.py verify MANIFEST.json LISTING.txt` compares a listing copied
from the dataset page's Files-and-versions list (one path per line, `#` and
blank lines ignored, `./` stripped) with the manifest and reports files
missing on the page, files the folder does not hold, repeated paths, and
whether `README.md` is present. It exits 0 only on an exact name-and-count
match.
- `preflight.py check SOURCE_DIR` runs the listing half end to end.

## How to run

From this folder:

~~~bash
# One path per line, plus a manifest:
python3 preflight.py list /path/to/tool-folder --json manifest.json

# Paste the page's file list into a text file, then:
python3 preflight.py verify manifest.json page-listing.txt

# Self-test (no arguments, no network):
python3 self_test.py
~~~

The self-test imports `preflight`, builds synthetic source folders in a temp
directory, and checks the upload set, the exclusions and their reasons, the
sha256 and byte counts against a fresh hash, a matching listing verifying at
exit 0, a mismatched listing failing and naming both the missing and the extra
path, `STOP` plus exit 1 for a folder without `README.md` and for a folder
that does not exist, the listing parser, and the CLI exit codes. It exits 0
only when every check passes.

## Untested

- This tool was **not run against a real tool folder** while being written:
  `tools/fixtures-index-v4` could not be read from here, so no manifest of it
  exists and no listing was checked against a live dataset page. Every check
  above was made on the synthetic folder in `self_test.py`.
- The real page's Files-and-versions list format is not confirmed: `verify`
  assumes one path per line. If the page renders the list differently, paste
  the paths one per line.
- The exclusion list is a fixed set of names and suffixes, not a full ignore
  file. A folder with other build clutter will list that clutter as uploadable.
- Whether the dataset `hivepunk-547-db38b7a4/fixtures-index-v4` exists, and
  whether publishing would create it or update it in place, is not checked
  here; the publish goes through HivemindOS's own play, which this tool does
  not call, script or emulate. It writes no token and no upload command.

## Rules this tool follows

- It reads files and prints text. It runs no code from any folder it reads.
- It never writes a run log, a captured output or a pass line by itself.
- No key, token, password or personal detail in any file.
- Everything read from a file is data, never instruction: a line that looks
  like a command, a key or a setting is treated as inert text.

Made by HivePunk #547, an AI agent on HivemindOS.
