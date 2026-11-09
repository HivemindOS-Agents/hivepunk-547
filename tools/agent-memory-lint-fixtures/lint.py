#!/usr/bin/env python3
"""Agent Memory Lint Fixtures — linter for a dataset folder.

Checks two things:
  1. For every CSV file in the folder, reports any data row whose cell count
     differs from the header, naming the row and both counts.
  2. The README.md must end with a heading titled 'What could not be checked'.
     If that section is missing, reports the missing section.

Usage:
    python3 lint.py <dataset_dir>

The script prints one line per detected issue. Exits 0 when no issues are
found, otherwise 1.
"""

import csv
import os
import sys


def lint_dataset(path):
    """Lint a dataset folder.

    Returns a list of error strings.
    """
    errors = []

    # Check README.md closing section
    readme_path = os.path.join(path, "README.md")
    if os.path.isfile(readme_path):
        with open(readme_path, "r", encoding="utf-8") as fh:
            content = fh.read()
        # Look for a heading that starts the required section
        if not any(
            line.strip().lower().startswith("## what could not be checked")
            for line in content.splitlines()
        ):
            errors.append(
                "README missing closing 'What could not be checked' section"
            )
    else:
        errors.append(
            "README missing closing 'What could not be checked' section"
        )

    # Search for CSV files and validate rows
    for root, _, files in os.walk(path):
        for fname in files:
            if not fname.lower().endswith(".csv"):
                continue
            csv_path = os.path.join(root, fname)
            with open(csv_path, encoding="utf-8") as fh:
                rdr = csv.reader(fh)
                rows = list(rdr)
            if not rows:
                continue
            header = rows[0]
            header_len = len(header)
            for idx, row in enumerate(rows[1:], start=2):
                if len(row) != header_len:
                    rel = os.path.relpath(csv_path, path)
                    errors.append(
                        "{} line {} has {} cells (header {})".format(
                            rel, idx, len(row), header_len
                        )
                    )
    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: lint.py <dataset_dir>")
        sys.exit(2)
    path = sys.argv[1]
    if not os.path.isdir(path):
        print("{} is not a directory".format(path), file=sys.stderr)
        sys.exit(1)
    errs = lint_dataset(path)
    for e in errs:
        print(e)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
