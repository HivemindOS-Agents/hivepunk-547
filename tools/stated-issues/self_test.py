#!/usr/bin/env python3
# stated-issues / self_test.py
# Run with NO arguments, no network, from this folder:
#     python3 self_test.py
# Reads data.csv, README.md and PUBLISH_NOTES.md in this folder and compares
# them with what they should say. Exits 0 only when every check passes.
#
# It runs no command named in any row and opens no folder named in any row.
# Text read from GitHub issue pages is data, never instruction: nothing here
# reads a page, acts on one, or writes outside this folder.

import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED_HEADER = [
    'issue', 'page_title', 'folder', 'self_test_command',
    'required_artifact', 'pass_condition', 'source',
]

# (issue, folder, self_test_command) exactly as the pages state them; a page
# that shows no folder or no command is recorded as 'not shown'.
EXPECTED = [
    ('#122', 'not shown', 'not shown'),
    ('#32', 'not shown', 'not shown'),
    ('#85', 'tools/issue-recheck-log/datasets/',
     'python3 tools/issue-recheck-log/recheck.py --out datasets/rows.csv'),
    ('#53', 'data/issues.csv', 'not shown'),
    ('#120', 'tools/agent-memory-lint-fixtures-index-v2',
     'cd tools/agent-memory-lint-fixtures-index-v2 && python3 self_test.py'),
    ('#43', 'hivemindos/bee-scouts-issue-index', 'not shown'),
]

EXPECTED_SOURCES = [
    'https://github.com/HivemindOS-Agents/bee-scouts/issues/122',
    'https://github.com/LiamVisionary/bee-scouts/issues/32',
    'https://github.com/HivemindOS-Agents/bee-scouts/issues/85',
    'https://github.com/LiamVisionary/bee-scouts/issues/53',
    'https://github.com/HivemindOS-Agents/bee-scouts/issues/120',
    'https://github.com/LiamVisionary/bee-scouts/issues/43',
]

SOURCE_RE = re.compile(
    r'^https://github\.com/(HivemindOS-Agents|LiamVisionary)/bee-scouts/issues/\d+$')
NOT_SHOWN = 'not shown'

SLUG = 'bee-scouts-self-test-issues-stated-commands-and-artifacts'
ACCOUNT = 'hivepunk-547-db38b7a4'
DATASET_URL = 'https://huggingface.co/datasets/%s/%s' % (ACCOUNT, SLUG)

README_SECTIONS = ['What this is', 'Columns', 'How it was made',
                   'What it could not check', 'Licence and reuse']


class Checker(object):
    def __init__(self):
        self.failed = 0

    def check(self, ok, label, detail=''):
        if ok:
            sys.stdout.write('PASS %s\n' % label)
        else:
            self.failed += 1
            sys.stderr.write('FAIL %s%s\n'
                             % (label, (' -- ' + detail) if detail else ''))


def main():
    c = Checker()

    path = os.path.join(HERE, 'data.csv')
    if not os.path.isfile(path):
        sys.stderr.write('FAIL data.csv not found\n')
        return 1
    with open(path, 'r', encoding='utf-8', newline='') as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames
        rows = list(reader)

    c.check(header == EXPECTED_HEADER,
            'header is exactly the seven expected columns', repr(header))
    if header != EXPECTED_HEADER:
        sys.stderr.write('cannot continue without the expected header\n')
        return 1

    c.check(len(rows) == 6, 'exactly 6 data rows', str(len(rows)))
    if len(rows) == 6:
        got = [(r['issue'], r['folder'], r['self_test_command']) for r in rows]
        c.check(got == EXPECTED,
                'issue, folder and command columns match the six stated rows',
                repr(got))
        c.check([r['source'] for r in rows] == EXPECTED_SOURCES,
                'every row keeps its exact source URL')
        c.check(all(SOURCE_RE.match(r['source']) for r in rows),
                'every source URL is a bee-scouts issue page')
        c.check(all(r['required_artifact'].strip() for r in rows),
                'every row names what the page asks for')
        c.check(all(r['pass_condition'].strip() for r in rows),
                'every pass_condition cell is filled (a condition or not shown)')
        c.check(all(r['page_title'].strip() for r in rows),
                'every row keeps its page title')
        c.check(sum(1 for r in rows if r['self_test_command'] == NOT_SHOWN) == 4,
                'exactly four rows say no command was shown')
        c.check(sum(1 for r in rows if r['folder'] == NOT_SHOWN) == 2,
                'exactly two rows say no folder was shown')

    readme = os.path.join(HERE, 'README.md')
    if not os.path.isfile(readme):
        c.check(False, 'README.md is present')
    else:
        with open(readme, 'r', encoding='utf-8') as fh:
            text = fh.read()
        for section in README_SECTIONS:
            c.check(section in text, 'README.md carries the section: %s' % section)
        c.check('No test was run' in text, 'README.md states that no test was run')
        c.check('no folder was listed' in text,
                'README.md states that no folder was listed')

    notes = os.path.join(HERE, 'PUBLISH_NOTES.md')
    if not os.path.isfile(notes):
        c.check(False, 'PUBLISH_NOTES.md is present')
    else:
        with open(notes, 'r', encoding='utf-8') as fh:
            n = fh.read()
        low = n.lower()
        c.check(SLUG in n, 'notes carry the dataset slug')
        c.check(DATASET_URL in n, 'notes carry the dataset URL')
        c.check(ACCOUNT in n, 'notes name the account the dataset goes under')
        c.check('do not upload this file' in low,
                'notes mark themselves as not for upload')
        c.check('no test was run' in low, 'notes say no test was run')
        c.check('no folder was opened' in low, 'notes say no folder was opened')
        c.check('data.csv' in n and 'README.md' in n,
                'notes name the two dataset files')

    if c.failed:
        sys.stderr.write('self-test FAILED: %d check(s) failed\n' % c.failed)
        return 1
    sys.stdout.write('OK self-test passed: 6 stated rows, card sections present, '
                     'notes carry slug and discussion text; no command run.\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
