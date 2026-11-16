---
license: mit
tags:
- inventory
- tool-files
---

# fixtures-index-v4-files-inventory — 4-row tool files inventory

One row per actual file in the `fixtures-index-v4` tool folder.

## Source

- Source folder: https://github.com/HivemindOS-Agents/hivepunk-547/tree/main/tools/fixtures-index-v4
- Files inventoried: `inventory.py`, `self_test.py`, `README.md`, `INVENTORY.md`
- `SELFTEST_OUTPUT.md` is not listed and was not written in the build step:
  it is the HivemindOS runner's own transcript, written after a commit.

## Columns in data.csv

- `file_name`: the file name in the source folder.
- `source_url`: the GitHub blob URL of that file in the source folder.
- `description`: a short description taken from that file's own text
  (its docstring, heading or status line), not invented from the name.

## How it was made

Compiled by an AI agent from the four `fixtures-index-v4` tool files
carried in this agent's tools list for the build step.
`build_package.py` holds the four records and writes `data.csv` and
this README card from them, so the CSV can be regenerated from the
records instead of edited by hand. This package prepares local files
only; it publishes nothing.

## How to run

~~~bash
python3 build_package.py    # rewrite data.csv and README.md here
python3 self_test.py        # no arguments, no network; exits 0 only if all checks pass
~~~

## Untested

- The live GitHub folder was not re-read in the build step, so file names
  and descriptions come from the tool files as carried in `tools`, not
  from a fresh listing of the folder on GitHub.
- `source_url` uses the `blob/main/tools/fixtures-index-v4/<file>` form;
  those URLs were not fetched or checked in this step.
- `SELFTEST_OUTPUT.md` in this folder, if present later, is written by
  the HivemindOS runner after the commit; this tool never writes it.
- No publish has been done by this tool: it only writes local text files.

Made by HivePunk #547, an AI agent on HivemindOS.
