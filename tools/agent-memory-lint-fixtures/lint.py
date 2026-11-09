~~~python
#!/usr/bin/env python3
import os
import sys
import csv


def lint_dataset(path):
    """Lint a dataset folder.
    Reports two issues:
      1. CSV rows whose cell count differs from the header.
      2. README.md missing a closing "What could not be checked" section.
    Returns a list of error strings.
    """
    errors = []

    # Check README.md closing section
    readme_path = os.path.join(path, "README.md")
    missing_close_section = False
    if os.path.isfile(readme_path):
        with open(readme_path, "r", encoding="utf-8") as fh:
            content = fh.read()
        # Look for a heading that starts the required section
        if not any(line.strip().lower().startswith("## what could not be checked") for line in content.splitlines()):
            missing_close_section = True
    else:
        missing_close_section = True
    if missing_close_section:
        errors.append("README missing closing 'What could not be checked' section")

    # Search for CSV files and validate rows
    for root, _, files in os.walk(path):
        for fname in files:
            if fname.lower().endswith('.csv'):
                csv_path = os.path.join(root, fname)
                with open(csv_path, encoding='utf-8') as fh:
                    rdr = csv.reader(fh)
                    rows = list(rdr)
                if not rows:
                    continue
                header = rows[0]
                header_len = len(header)
                for idx, row in enumerate(rows[1:], start=2):
                    if len(row) != header_len:
                        rel = os.path.relpath(csv_path, path)
                        errors.append(f"{rel} line {idx} has {len(row)} cells (header {header_len})")
    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: lint.py <dataset_dir>")
        sys.exit(2)
    path = sys.argv[1]
    if not os.path.isdir(path):
        print(f"{path} is not a directory", file=sys.stderr)
        sys.exit(1)
    errs = lint_dataset(path)
    for e in errs:
        print(e)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
~~~
