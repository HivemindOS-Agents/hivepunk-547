#!/usr/bin/env python3
"""Dataset Card Lint — checks a folder's README card and CSV consistency.

Usage:
    python3 lint.py <dataset_dir>

Returns:
    Exit code 0 if no issues found.
    Exit code 1 if any issues are found (prints one line per issue).
    Exit code 2 for invalid arguments.
"""

import csv
import os
import sys


def lint_dataset(path):
    """Lint a dataset folder.

    Returns a list of error strings (empty means all good).
    """
    errors = []

    # Check 1: README.md must have a closing 'What could not be checked' heading
    readme_path = os.path.join(path, "README.md")
    if os.path.isfile(readme_path):
        with open(readme_path, "r", encoding="utf-8") as fh:
            content = fh.read()
        # Look for any line that starts with '## what could not be checked' (case-insensitive)
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

    # Check 2: every CSV row must have the same number of cells as its header
    for root, _, files in os.walk(path):
        for fname in files:
            if not fname.lower().endswith(".csv"):
                continue
            csv_path = os.path.join(root, fname)
            with open(csv_path, encoding="utf-8", newline="") as fh:
                reader = csv.reader(fh)
                rows = list(reader)
            if not rows:
                continue
            header_len = len(rows[0])
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
        print("Usage: {} <dataset_dir>".format(sys.argv[0]), file=sys.stderr)
        sys.exit(2)
    path = sys.argv[1]
    if not os.path.isdir(path):
        print("Error: {} is not a directory".format(path), file=sys.stderr)
        sys.exit(2)
    errors = lint_dataset(path)
    for e in errors:
        print(e)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
