#!/usr/bin/env python3
"""memory_lint_check.py: validate agent-memory lint fixture files.

Usage (from this folder):
    python3 memory_lint_check.py FIXTURES.json
    python3 memory_lint_check.py FIXTURES.jsonl
    python3 memory_lint_check.py FIXTURES.json --strict

Fixture formats (auto-detected by extension, then content):
  * JSON (.json): a list of fixture objects, or an object with a
    "fixtures" (or "cases", "items", "entries") list.
  * JSONL (.jsonl, .ndjson): one JSON object per non-blank line.
  * Extensionless/other: JSON if the file starts with [ or {,
    otherwise JSONL.

Each fixture must be an object with:
  * id: non-empty string, unique across the file, safe as a name
  * prompt: non-empty string (after stripping whitespace)
  * expected: non-empty string, or a non-empty list of non-empty
    strings (also accepts the field name "expect" or "output"
    as an alias, checked in that order)

Optional path-like fields (path, file, filepath, filename, ref,
source): if present and non-empty, their value must be a relative
path that does not escape its base (no absolute path, no '..'
segment, no backslash-separated '..' segment) and must not be
empty after stripping. The id itself is also checked the same
way when it looks path-like (contains '/' or '\\').

Checks are read-only, no network, writes nothing. Prints counts
and a PASS/FAIL summary, e.g.:
  PASS: fixtures.json (fixtures: 3, valid: 3, invalid: 0)
With --strict, duplicate ids also fail; by default duplicates
are reported as FAIL problems as well (a duplicate id is an
invalid fixture), so --strict additionally rejects alias-field
fixtures that have no "expected" field at all only when the
fixture has no usable expected value. In practice --strict is
reserved for future tightening and currently behaves like the
default check; it is accepted for compatibility.
On failure prints one FAIL line per problem plus a FAIL summary
and exits 1; on success prints PASS and exits 0.
"""

import json
import os
import sys

LIST_FIELDS = ("fixtures", "cases", "items", "entries")
EXPECTED_FIELDS = ("expected", "expect", "output")
PATH_FIELDS = ("path", "file", "filepath", "filename", "ref", "source")


def _is_unsafe_path(value):
    if not isinstance(value, str):
        return True
    text = value.strip()
    if not text:
        return True
    if os.path.isabs(text) or text.startswith("/") or text.startswith("\\"):
        return True
    if len(text) >= 2 and text[1] == ":" and text[0].isalpha():
        return True
    parts = text.replace("\\", "/").split("/")
    return any(part == ".." for part in parts)


def _expected_value(fixture):
    for key in EXPECTED_FIELDS:
        if key in fixture:
            return fixture.get(key), key
    return None, None


def _expected_ok(value):
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value) and all(isinstance(v, str) and v.strip() for v in value)
    return False


def parse_fixtures(path):
    """Return list of fixture objects. Raises ValueError/OSError."""
    with open(path, encoding="utf-8-sig") as fh:
        text = fh.read()
    if not text.strip():
        raise ValueError("fixture file is empty")
    ext = os.path.splitext(path)[1].lower()
    stripped = text.strip()
    if ext in (".jsonl", ".ndjson") or (ext not in (".json",) and not stripped.startswith(("[", "{"))):
        out = []
        for lineno, line in enumerate(text.splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except ValueError as e:
                raise ValueError("line %d is not valid JSON: %s" % (lineno, e))
            if not isinstance(obj, dict):
                raise ValueError("line %d must be a JSON object" % lineno)
            out.append(obj)
        return out
    data = json.loads(text) if ext != ".json" or stripped.startswith(("[", "{")) else json.loads(text)
    items = None
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        for key in LIST_FIELDS:
            if isinstance(data.get(key), list):
                items = data[key]
                break
        if items is None:
            if "id" in data or "prompt" in data:
                items = [data]
    if items is None:
        raise ValueError("JSON fixture file must be a list, an object with a fixtures/cases list, or a single fixture object")
    for i, item in enumerate(items, 1):
        if not isinstance(item, dict):
            raise ValueError("fixture %d must be an object" % i)
    return items


def check(fixture_path, strict=False):
    """Return (ok, problems, notes, counts dict)."""
    problems = []
    notes = []
    counts = {"fixtures": 0, "valid": 0, "invalid": 0}
    if not os.path.exists(fixture_path):
        problems.append("%s: fixture file not found: %s" % (fixture_path, fixture_path))
        return False, problems, notes, counts
    if not os.path.isfile(fixture_path):
        problems.append("%s: fixture path is not a file: %s" % (fixture_path, fixture_path))
        return False, problems, notes, counts
    try:
        fixtures = parse_fixtures(fixture_path)
    except (OSError, UnicodeError) as e:
        problems.append("%s: could not read fixture file: %s: %s" % (fixture_path, type(e).__name__, e))
        return False, problems, notes, counts
    except ValueError as e:
        problems.append("%s: invalid fixture file: %s" % (fixture_path, e))
        return False, problems, notes, counts
    counts["fixtures"] = len(fixtures)
    if not fixtures:
        problems.append("%s: fixture file contains no fixtures" % fixture_path)
        return False, problems, notes, counts
    seen = {}
    for idx, fx in enumerate(fixtures, 1):
        label = "fixture %d" % idx
        before = len(problems)
        fid = fx.get("id")
        if fid is None:
            problems.append("%s: %s: missing required field 'id'" % (fixture_path, label))
        elif not isinstance(fid, str) or not fid.strip():
            problems.append("%s: %s: field 'id' must be a non-empty string" % (fixture_path, label))
        else:
            fid = fid.strip()
            label = "fixture %d (id=%s)" % (idx, fid)
            if fid in seen:
                problems.append("%s: %s: duplicate id '%s' (first at fixture %d)" % (fixture_path, label, fid, seen[fid]))
            else:
                seen[fid] = idx
            if ("/" in fid or "\\" in fid) and _is_unsafe_path(fid):
                problems.append("%s: %s: id is an unsafe path: %r" % (fixture_path, label, fid))
        prompt = fx.get("prompt")
        if prompt is None:
            problems.append("%s: %s: missing required field 'prompt'" % (fixture_path, label))
        elif not isinstance(prompt, str):
            problems.append("%s: %s: field 'prompt' must be a string" % (fixture_path, label))
        elif not prompt.strip():
            problems.append("%s: %s: field 'prompt' is empty" % (fixture_path, label))
        value, key = _expected_value(fx)
        if key is None:
            problems.append("%s: %s: missing required field 'expected'" % (fixture_path, label))
        elif not _expected_ok(value):
            problems.append("%s: %s: field '%s' must be a non-empty string or a non-empty list of non-empty strings" % (fixture_path, label, key))
        for field in PATH_FIELDS:
            if field in fx and fx.get(field) not in (None, ""):
                pval = fx.get(field)
                if not isinstance(pval, str) or _is_unsafe_path(pval):
                    problems.append("%s: %s: field '%s' is an unsafe path: %r" % (fixture_path, label, field, pval))
        if len(problems) == before:
            counts["valid"] += 1
        else:
            counts["invalid"] += 1
    if strict:
        notes.append("strict mode on (same checks as default for this version)")
    return not problems, problems, notes, counts


def _fmt(counts):
    return "fixtures: %d, valid: %d, invalid: %d" % (counts["fixtures"], counts["valid"], counts["invalid"])


def main(argv):
    args = list(argv[1:])
    strict = False
    fixture = None
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--strict":
            strict = True; i += 1
        elif arg in ("-h", "--help"):
            print(__doc__.strip()); return 0
        elif arg.startswith("--"):
            print("FAIL: unknown option %s" % arg); return 1
        elif fixture is None:
            fixture = arg; i += 1
        else:
            print("FAIL: unexpected extra argument %s" % arg); return 1
    if not fixture:
        print("FAIL: usage: python3 memory_lint_check.py FIXTURES.json [--strict]")
        return 1
    ok, problems, notes, counts = check(fixture, strict=strict)
    for note in notes:
        print("NOTE: " + note)
    if ok:
        print("PASS: %s (%s)" % (fixture, _fmt(counts)))
        return 0
    for p in problems:
        print("FAIL: " + p)
    print("FAIL: %s (%s)" % (fixture, _fmt(counts)))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
