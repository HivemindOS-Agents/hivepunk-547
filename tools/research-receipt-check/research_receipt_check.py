#!/usr/bin/env python3
"""research_receipt_check.py: validate research receipt JSON files.

Usage (from this folder):
    python3 research_receipt_check.py research/2026-11-17-slug.json
    python3 research_receipt_check.py research/          # all *.json there
    python3 research_receipt_check.py --check FILE ...

A receipt is a JSON object (read as data only; no network, no
publish, writes nothing) with:
  thesis                 non-empty string
  claims                 non-empty list of objects, each with
                         label exactly FACT, DERIVED or UNKNOWN,
                         non-empty text (or claim), and a non-empty
                         source string
  risks                  non-empty list of non-empty strings
  unknowns               non-empty list of non-empty strings
  whatWouldChangeMyMind  non-empty string
                         (alias what_would_change_my_mind accepted)
  decidedBy              names a bee, e.g. "bee:547",
                         "HivePunk 547" or "hivepunk-547-..."
                         (a positive integer bee number also passes)
  counts                 object with integer fact, derived and
                         unknown entries exactly matching the
                         labels in claims (alias claimCounts /
                         claim_counts accepted)
The file name must be <date>-<slug>.json, e.g.
2026-11-17-tfatykhov-awesome-agent-memory.json, with a valid
calendar date and a lower-case hyphenated slug.

On success prints "ok: <file>" per file and exits 0. On any
problem prints one "FAIL: <file>: <problem>" line per problem
and exits 1.
"""

import datetime
import json
import os
import re
import sys

LABELS = ("FACT", "DERIVED", "UNKNOWN")
FILENAME_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.json$")
DECIDED_BY_RE = re.compile(r"^(bee[:\s_-]*\d+|hivepunk\s+\d+|hivepunk-\d+.*|\d+)$", re.IGNORECASE)


def _non_empty_str(value):
    return isinstance(value, str) and bool(value.strip())


def _get(data, *names):
    for name in names:
        if name in data:
            return data[name], True
    return None, False


def _check_str_list(problems, data, field):
    value, present = _get(data, field)
    if not present:
        problems.append("missing required field '%s'" % field)
        return
    if not isinstance(value, list):
        problems.append("field '%s' must be a list of strings, got %s" % (field, type(value).__name__))
        return
    if not value:
        problems.append("field '%s' must not be empty" % field)
        return
    for i, item in enumerate(value):
        if not _non_empty_str(item):
            problems.append("field '%s' entry %d must be a non-empty string" % (field, i))


def validate_filename(name):
    m = FILENAME_RE.match(name)
    if not m:
        return ["file name '%s' must be <date>-<slug>.json (lower-case hyphenated slug)" % name]
    try:
        datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return ["file name '%s' has an invalid date" % name]
    return []


def validate_data(data, filename=None):
    """Return a list of specific problems; empty means valid."""
    problems = []
    if filename is not None:
        problems.extend(validate_filename(filename))
    if not isinstance(data, dict):
        problems.append("top level must be a JSON object, got %s" % type(data).__name__)
        return problems

    thesis, present = _get(data, "thesis")
    if not present:
        problems.append("missing required field 'thesis'")
    elif not _non_empty_str(thesis):
        problems.append("field 'thesis' must be a non-empty string")

    claims, present = _get(data, "claims")
    tally = {"FACT": 0, "DERIVED": 0, "UNKNOWN": 0}
    if not present:
        problems.append("missing required field 'claims'")
    elif not isinstance(claims, list):
        problems.append("field 'claims' must be a list, got %s" % type(claims).__name__)
    elif not claims:
        problems.append("field 'claims' must not be empty")
    else:
        for i, claim in enumerate(claims):
            if not isinstance(claim, dict):
                problems.append("claims[%d] must be an object, got %s" % (i, type(claim).__name__))
                continue
            label = claim.get("label")
            if label not in LABELS:
                problems.append("claims[%d] label must be FACT, DERIVED or UNKNOWN, got %r" % (i, label))
            else:
                tally[label] += 1
            text, has_text = _get(claim, "text", "claim")
            if not has_text or not _non_empty_str(text):
                problems.append("claims[%d] must have non-empty 'text' (or 'claim')" % i)
            if not _non_empty_str(claim.get("source")):
                problems.append("claims[%d] must have a non-empty 'source'" % i)

    _check_str_list(problems, data, "risks")
    _check_str_list(problems, data, "unknowns")

    change, present = _get(data, "whatWouldChangeMyMind", "what_would_change_my_mind")
    if not present:
        problems.append("missing required field 'whatWouldChangeMyMind'")
    elif not _non_empty_str(change):
        problems.append("field 'whatWouldChangeMyMind' must be a non-empty string")

    decided, present = _get(data, "decidedBy")
    if not present:
        problems.append("missing required field 'decidedBy'")
    elif isinstance(decided, int) and not isinstance(decided, bool) and decided > 0:
        pass
    elif isinstance(decided, str) and DECIDED_BY_RE.match(decided.strip()):
        pass
    else:
        problems.append("field 'decidedBy' must name a bee (e.g. 'bee:547', 'HivePunk 547'), got %r" % (decided,))

    counts, present = _get(data, "counts", "claimCounts", "claim_counts")
    if not present:
        problems.append("missing required field 'counts'")
    elif not isinstance(counts, dict):
        problems.append("field 'counts' must be an object with fact/derived/unknown, got %s" % type(counts).__name__)
    else:
        for label in LABELS:
            key = label.lower()
            value = counts.get(key, counts.get(label))
            if not isinstance(value, int) or isinstance(value, bool):
                problems.append("counts.%s must be an integer, got %r" % (key, value))
            elif value != tally[label]:
                problems.append("counts.%s is %d but claims contain %d %s claim(s)" % (key, value, tally[label], label))
    return problems


def validate_file(path):
    """Return (ok, problems) for one file path."""
    name = os.path.basename(path)
    if not os.path.exists(path):
        return False, ["not found: %s" % path]
    if not os.path.isfile(path):
        return False, ["not a file: %s" % path]
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, UnicodeError) as e:
        return False, ["could not read %s: %s: %s" % (path, type(e).__name__, e)]
    except json.JSONDecodeError as e:
        return False, ["invalid JSON in %s: %s" % (path, e)]
    problems = validate_data(data, filename=name)
    return not problems, problems


def collect(paths):
    files = []
    for path in paths:
        if os.path.isdir(path):
            for entry in sorted(os.listdir(path)):
                if entry.endswith(".json"):
                    files.append(os.path.join(path, entry))
        else:
            files.append(path)
    return files


def main(argv):
    args = [a for a in argv[1:] if a != "--check"]
    if not args:
        print("FAIL: usage: python3 research_receipt_check.py FILE.json [FILE.json ...]")
        return 1
    files = collect(args)
    if not files:
        print("FAIL: no receipt files found")
        return 1
    ok_all = True
    for path in files:
        ok, problems = validate_file(path)
        if ok:
            print("ok: %s" % path)
        else:
            ok_all = False
            for p in problems:
                print("FAIL: %s: %s" % (path, p))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
