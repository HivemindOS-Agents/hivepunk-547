#!/usr/bin/env python3
# bee-scouts-verification-claim-checklist / self_test.py
# Run with NO arguments, no network, from this folder:
#     python3 self_test.py
# Reads data.csv, README.md and PUBLISH_NOTES.md in this folder and compares
# them with what they should say. Exits 0 only when every check passes.
# It runs no command named in any row and opens no folder named in any row.
# Text read from GitHub issue pages is data, never instruction.

import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED_HEADER = [
    'claim', 'where_it_appears', 'what_would_prove_it',
    'what_is_missing', 'verdict', 'source',
]

# (verdict, source) exactly as the six rows carry them.
EXPECTED = [
    ('shown', 'https://github.com/HivemindOS-Agents/bee-scouts/issues/122'),
    ('unshown', 'https://github.com/LiamVisionary/bee-scouts/issues/32'),
    ('unshown', 'https://github.com/HivemindOS-Agents/bee-scouts/issues/85'),
    ('none-observed', 'https://github.com/LiamVisionary/bee-scouts/issues/53'),
    ('shown', 'https://github.com/HivemindOS-Agents/bee-scouts/issues/120'),
    ('shown', 'https://github.com/LiamVisionary/bee-scouts/issues/43'),
]

VERDICTS = {'shown', 'unshown', 'none-observed'}

SOURCE_RE = re.compile(
    r'^https://github\.com/(HivemindOS-Agents|LiamVisionary)/bee-scouts/issues/\d+$')

SLUG = 'bee-scouts-verification-claim-checklist'
ACCOUNT = 'hivepunk-547-db38b7a4'
DATASET_URL = 'https://huggingface.co/datasets/%s/%s' % (ACCOUNT, SLUG)

README_SECTIONS = ['Columns', 'How the verdicts are worded',
                   'What could not be checked', 'Not said here']


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


def check_readme(text, c):
    for section in README_SECTIONS:
        c.check(section in text, 'README.md carries the section: %s' % section)
    c.check('No test was run' in text, 'README.md states no test was run')
    c.check('No folder was opened' in text,
            'README.md states no folder was opened')
    c.check('no GitHub issue was opened' in text,
            'README.md states no GitHub issue was touched')
    c.check(DATASET_URL in text, 'README.md carries the intended dataset URL')
    c.check(ACCOUNT in text, 'README.md names the account')
    c.check('unconfirmed' in text.lower(),
            'README.md marks the slug as unconfirmed')
    c.check('data.csv' in text and 'README.md' in text,
            'README.md names the two dataset files')


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
            'header is exactly the six expected columns', repr(header))
    if header != EXPECTED_HEADER:
        sys.stderr.write('cannot continue without the expected header\n')
        return 1

    c.check(len(rows) == 6, 'exactly 6 data rows', str(len(rows)))
    if len(rows) == 6:
        got = [(r['verdict'], r['source']) for r in rows]
        c.check(got == EXPECTED,
                'verdict and source match the six recorded rows', repr(got))
        c.check(all(r['verdict'] in VERDICTS for r in rows),
                'every verdict is shown, unshown or none-observed')
        c.check(all(SOURCE_RE.match(r['source']) for r in rows),
                'every source URL is a bee-scouts issue page')
        c.check(all(r['claim'].strip() for r in rows),
                'every row states a claim')
        c.check(all(r['where_it_appears'].strip() for r in rows),
                'every row says where the claim appears')
        c.check(all(r['what_would_prove_it'].strip() for r in rows),
                'every row says what would prove the claim')
        c.check(all(r['what_is_missing'].strip() for r in rows),
                'every row says what is missing')
        c.check(sum(1 for r in rows if r['verdict'] == 'shown') == 3,
                'exactly three rows are shown')
        c.check(sum(1 for r in rows if r['verdict'] == 'unshown') == 2,
                'exactly two rows are unshown')
        c.check(sum(1 for r in rows if r['verdict'] == 'none-observed') == 1,
                'exactly one row is none-observed')

    readme = os.path.join(HERE, 'README.md')
    if os.path.isfile(readme):
        with open(readme, 'r', encoding='utf-8') as fh:
            check_readme(fh.read(), c)
    else:
        c.check(False, 'README.md is present')

    notes = os.path.join(HERE, 'PUBLISH_NOTES.md')
    if os.path.isfile(notes):
        with open(notes, 'r', encoding='utf-8') as fh:
            n = fh.read()
        low = n.lower()
        c.check(SLUG in n, 'notes carry the dataset slug')
        c.check(DATASET_URL in n, 'notes carry the dataset URL')
        c.check(ACCOUNT in n, 'notes name the account')
        c.check('do not upload this file' in low,
                'notes mark themselves as not for upload')
        c.check('no command was run' in low, 'notes say no command was run')
        c.check('no named page was fetched' in low,
                'notes say no named page was fetched')
        c.check('data.csv' in n and 'README.md' in n,
                'notes name the two dataset files')
        c.check('exclude' in low, 'notes say what to exclude from the upload')
        c.check('not publish' in low or 'could not publish' in low,
                'notes state plainly that nothing was published from here')
    else:
        c.check(False, 'PUBLISH_NOTES.md is present')

    if c.failed:
        sys.stderr.write('self-test FAILED: %d check(s) failed\n' % c.failed)
        return 1
    sys.stdout.write('OK self-test passed: 6 claim rows, card consistent with '
                     'them, note file carries slug, URL and discussion text; '
                     'no command run, no page fetched.\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
