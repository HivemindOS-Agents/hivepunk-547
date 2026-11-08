#!/usr/bin/env python3
# self_test.py for stated-issues tool
# Run with NO arguments, no network, from this directory.
# Reads data.csv and README.md and checks their structure.
# Exits 0 only when every check passes.

import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED_HEADER = [
    'issue', 'page_title', 'folder', 'self_test_command',
    'required_artifact', 'pass_condition', 'source'
]

EXPECTED_ISSUES = ['#122', '#32', '#85', '#53', '#120', '#43']

SOURCE_RE = re.compile(
    r'^https://github\.com/(HivemindOS-Agents|LiamVisionary)/bee-scouts/issues/\d+$'
)

def read_csv():
    path = os.path.join(HERE, 'data.csv')
    if not os.path.isfile(path):
        sys.stderr.write('FAIL data.csv not found\n')
        return None
    with open(path, 'r', encoding='utf-8', newline='') as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames
        rows = list(reader)
    return header, rows

def check():
    problems = []

    csv_data = read_csv()
    if csv_data is None:
        problems.append('data.csv not found')
    else:
        header, rows = csv_data
        if header != EXPECTED_HEADER:
            problems.append('header mismatch: got %r' % header)
        if len(rows) != 6:
            problems.append('expected 6 rows, got %d' % len(rows))
        else:
            for i, row in enumerate(rows):
                if row['issue'] != EXPECTED_ISSUES[i]:
                    problems.append('row %d issue mismatch: got %s' % (i, row['issue']))
                if not row.get('page_title', '').strip():
                    problems.append('row %d missing page_title' % i)
                if not row.get('folder', '').strip():
                    problems.append('row %d missing folder' % i)
                if not row.get('self_test_command', '').strip():
                    problems.append('row %d missing self_test_command' % i)
                if not row.get('required_artifact', '').strip():
                    problems.append('row %d missing required_artifact' % i)
                if not row.get('pass_condition', '').strip():
                    problems.append('row %d missing pass_condition' % i)
                src = row.get('source', '')
                if not SOURCE_RE.match(src):
                    problems.append('row %d source invalid: %s' % (i, src))

    readme_path = os.path.join(HERE, 'README.md')
    if not os.path.isfile(readme_path):
        problems.append('README.md not found')
    else:
        with open(readme_path, 'r', encoding='utf-8') as fh:
            readme_content = fh.read()
        required_sections = [
            'What this is', 'Columns', 'How it was made',
            'What it could not check', 'Licence and reuse'
        ]
        for section in required_sections:
            if section not in readme_content:
                problems.append('README.md missing section: %s' % section)

    for p in problems:
        sys.stdout.write('FAIL %s\n' % p)
    if not problems:
        sys.stdout.write('PASS all checks passed: 6 rows, correct header, README sections\n')
    return len(problems)

if __name__ == '__main__':
    sys.exit(check())
