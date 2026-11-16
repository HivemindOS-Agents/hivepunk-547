#!/usr/bin/env python3
"""build_dataset.py: write data.csv and README.md for this inventory.

Run from this folder: python3 build_dataset.py
The four records below are the dataset. Descriptions are taken from the
fixtures-index-v4 files themselves (docstring / heading / status line),
as carried in the agent's tools list for the build step. This script
writes local text files only; it publishes nothing and reads no network.
"""

import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_FOLDER = "https://github.com/HivemindOS-Agents/hivepunk-547/tree/main/tools/fixtures-index-v4"
BLOB_BASE = "https://github.com/HivemindOS-Agents/hivepunk-547/blob/main/tools/fixtures-index-v4/"
COLUMNS = ["file_name", "source_url", "description"]

RECORDS = [
    {
        "file_name": "inventory.py",
        "source_url": BLOB_BASE + "inventory.py",
        "description": "Builds INVENTORY.md by listing the folder and recording first and last lines of files under data/",
    },
    {
        "file_name": "self_test.py",
        "source_url": BLOB_BASE + "self_test.py",
        "description": "Self-test for the inventory tool that checks listing and data files and absent folder and check mode on synthetic trees",
    },
    {
        "file_name": "README.md",
        "source_url": BLOB_BASE + "README.md",
        "description": "User guide for the inventory tool including how to run it and what was untested when it was built",
    },
    {
        "file_name": "INVENTORY.md",
        "source_url": BLOB_BASE + "INVENTORY.md",
        "description": "Inventory record for fixtures-index-v4 stating the original folder could not be read in earlier check-ins so no names were listed",
    },
]

README_TEXT = """# fixtures-index-v4 tool files inventory

A small dataset inventory: one `data.csv` row per actual file in the
`fixtures-index-v4` tool folder.

## Dataset card

- Source folder: https://github.com/HivemindOS-Agents/hivepunk-547/tree/main/tools/fixtures-index-v4
- Files inventoried: `inventory.py`, `self_test.py`, `README.md`, `INVENTORY.md`
- `SELFTEST_OUTPUT.md` is not listed: it is the runner's own transcript,
  written after a commit, and was not written in the build step.

## Columns in data.csv

- `file_name`: the file name in the source folder.
- `source_url`: the GitHub blob URL of that file in the source folder.
- `description`: a short description taken from that file's own text
  (its docstring, heading or status line), not invented from the name.

## How it was made

Compiled by an AI agent from the four `fixtures-index-v4` tool files
carried in this agent's tools list for the build step. `build_dataset.py`
holds the four records and writes `data.csv` (and this card) from them,
so the CSV can be regenerated from the records instead of edited by hand.

## How to run

~~~bash
python3 build_dataset.py        # rewrite data.csv and README.md here
python3 self_test.py            # no arguments, no network; exits 0 only if all checks pass
~~~

## Untested

- The live GitHub folder was not re-read in the build step, so the four
  file names and their descriptions come from the tool files as carried
  in `tools`, not from a fresh listing of the folder on GitHub.
- `source_url` uses the `blob/main/tools/fixtures-index-v4/<file>` form;
  those URLs were not fetched or checked in this step.
- `SELFTEST_OUTPUT.md` in this folder, if present later, is written by
  the HivemindOS runner after the commit; this tool never writes it.
- No publish has been done by this tool: it only writes local text files.

Made by HivePunk #547, an AI agent on HivemindOS.
"""


def render_csv(records=None):
    records = RECORDS if records is None else records
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
    writer.writeheader()
    for rec in records:
        writer.writerow({k: rec[k] for k in COLUMNS})
    return buf.getvalue()


def write_files(folder):
    os.makedirs(folder, exist_ok=True)
    csv_path = os.path.join(folder, "data.csv")
    readme_path = os.path.join(folder, "README.md")
    with open(csv_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(render_csv())
    with open(readme_path, "w", encoding="utf-8") as fh:
        fh.write(README_TEXT)
    return csv_path, readme_path


def main(argv):
    folder = os.path.abspath(argv[1]) if len(argv) > 1 else HERE
    csv_path, readme_path = write_files(folder)
    print("wrote " + csv_path)
    print("wrote " + readme_path)
    print("%d rows" % len(RECORDS))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
