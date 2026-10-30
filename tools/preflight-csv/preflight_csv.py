#!/usr/bin/env python3
# UNTESTED - run self_test.py to verify before using in production.
"""Preflight check for a local CSV file.

Usage:
    python3 preflight_csv.py <csv_file> '<expected_header_comma_separated>'

Checks (each gets a PASS/FAIL line):
- header_match: header row equals the expected field list exactly.
- field_count_consistency: every data row has the same number of fields as the header.
- no_empty_required: no cell in the data rows is empty.
- no_stray_whitespace: no cell in the data rows has leading or trailing whitespace.

Exit status: 0 if all rules pass, 1 otherwise.
"""

import sys
import csv

def preflight(csv_path, expected_header_str):
    expected_fields = expected_header_str.split(',')
    errors = {
        'header_match': False,
        'field_count_consistency': True,
        'no_empty_required': True,
        'no_stray_whitespace': True,
    }
    with open(csv_path, newline='') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            header = []

        # rule: header matches expected
        errors['header_match'] = (header == expected_fields)

        header_len = len(header)
        for row_num, row in enumerate(reader, start=2):
            # rule: field count consistency
            if len(row) != header_len:
                errors['field_count_consistency'] = False

            # rules: no empty required fields, no stray whitespace
            for field in row:
                if field == '':
                    errors['no_empty_required'] = False
                if field != field.strip():
                    errors['no_stray_whitespace'] = False

    return errors

def main():
    if len(sys.argv) != 3 or sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        sys.exit(1 if len(sys.argv) != 3 else 0)

    csv_file = sys.argv[1]
    expected_header = sys.argv[2]

    try:
        results = preflight(csv_file, expected_header)
    except FileNotFoundError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"FAIL: {e}")
        sys.exit(1)

    all_pass = True
    for rule, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"{rule}: {status}")
        if not passed:
            all_pass = False

    sys.exit(0 if all_pass else 1)

if __name__ == '__main__':
    main()
