#!/usr/bin/env python3
"""dataset_manifest_check.py: check a dataset manifest against local files.

Usage (from this folder):
    python3 dataset_manifest_check.py MANIFEST
    python3 dataset_manifest_check.py MANIFEST --root DIR
    python3 dataset_manifest_check.py MANIFEST --allow-unlisted
    python3 dataset_manifest_check.py MANIFEST --root DIR --quiet-unlisted

Manifest formats (auto-detected by extension or content):
  * JSON (.json): a list of entries, or an object with a "files"
    (or "file", "paths", "entries") list. Each entry is either a
    string path or an object with path/file/filename/name field.
  * CSV (.csv): a header row; the path column is the first of
    path, file, filename, name present in the header.
  * Text (.txt, .tsv, .md, or no/other extension): one path per
    line; blank lines and lines starting with # are ignored, and a
    leading "- " or "* " bullet marker is stripped.

Checks (read-only, no network, writes nothing):
  * every listed path exists under the root directory as a file;
  * listed paths may not escape the root (no ../ or absolute paths);
  * files under root that are not listed are flagged as unlisted,
    excluding the manifest file itself. Directories are walked
    recursively; symlinks to directories are not followed.

Prints counts and a PASS/FAIL summary, e.g.:
  PASS: manifest.txt (listed: 3, present: 3, missing: 0, unlisted: 0)
On failure prints one FAIL line per problem, then a FAIL summary
with the same counts, and exits 1. With --allow-unlisted, unlisted
files are reported as NOTE and do not fail the run.
"""

import csv
import io
import json
import os
import sys

PATH_FIELDS = ("path", "file", "filename", "name")
LIST_FIELDS = ("files", "file", "paths", "entries")
CSV_PATH_COLUMNS = ("path", "file", "filename", "name")


def _clean_entry(text):
    text = (text or "").strip()
    if text.startswith(("- ", "* ", "+ ")):
        text = text[2:].strip()
    return text.strip("`").strip()


def _entries_from_json(text):
    data = json.loads(text)
    items = None
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        for key in LIST_FIELDS:
            if isinstance(data.get(key), list):
                items = data[key]
                break
    if items is None:
        raise ValueError("JSON manifest must be a list or an object with a files/paths/entries list")
    out = []
    for i, item in enumerate(items, 1):
        if isinstance(item, str):
            out.append(_clean_entry(item))
        elif isinstance(item, dict):
            value = None
            for key in PATH_FIELDS:
                if item.get(key):
                    value = str(item[key])
                    break
            if value is None:
                raise ValueError("JSON entry %d has no path/file/filename/name field" % i)
            out.append(_clean_entry(value))
        else:
            raise ValueError("JSON entry %d must be a string or an object" % i)
    return out


def _entries_from_csv(text):
    reader = csv.reader(io.StringIO(text))
    rows = [row for row in reader if any((c or "").strip() for c in row)]
    if not rows:
        return []
    header = [(c or "").strip().lower() for c in rows[0]]
    col = None
    for candidate in CSV_PATH_COLUMNS:
        if candidate in header:
            col = header.index(candidate)
            break
    if col is None:
        raise ValueError("CSV manifest header must contain one of: %s (got: %s)" % (",".join(CSV_PATH_COLUMNS), ",".join(header)))
    out = []
    for lineno, row in enumerate(rows[1:], 2):
        if col < len(row) and (row[col] or "").strip():
            out.append(_clean_entry(row[col]))
    return out


def _entries_from_text(text):
    out = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        value = _clean_entry(stripped)
        if value:
            out.append(value)
    return out


def parse_manifest(path):
    """Return list of listed paths (strings). Raises ValueError/OSError."""
    with open(path, encoding="utf-8-sig") as fh:
        text = fh.read()
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        return _entries_from_json(text)
    if ext == ".csv":
        return _entries_from_csv(text)
    if ext in (".txt", ".tsv", ".md", ""):
        # Try JSON by content as a fallback for extensionless JSON.
        stripped = text.strip()
        if stripped.startswith("[") or stripped.startswith("{"):
            try:
                return _entries_from_json(text)
            except ValueError:
                pass
        return _entries_from_text(text)
    stripped = text.strip()
    if stripped.startswith("[") or stripped.startswith("{"):
        return _entries_from_json(text)
    return _entries_from_text(text)


def _is_unsafe(entry):
    if not entry:
        return True
    if os.path.isabs(entry):
        return True
    parts = entry.replace("\\", "/").split("/")
    return any(part in ("..",) for part in parts)


def check(manifest_path, root=None, allow_unlisted=False):
    """Return (ok, problems, notes, counts dict)."""
    problems = []
    notes = []
    counts = {"listed": 0, "present": 0, "missing": 0, "unlisted": 0}
    if not os.path.exists(manifest_path):
        problems.append("%s: manifest not found: %s" % (manifest_path, manifest_path))
        return False, problems, notes, counts
    if not os.path.isfile(manifest_path):
        problems.append("%s: manifest is not a file: %s" % (manifest_path, manifest_path))
        return False, problems, notes, counts
    if root is None:
        root = os.path.dirname(os.path.abspath(manifest_path))
    if not os.path.isdir(root):
        problems.append("%s: root is not a directory: %s" % (manifest_path, root))
        return False, problems, notes, counts
    root_abs = os.path.abspath(root)
    try:
        listed = parse_manifest(manifest_path)
    except (OSError, UnicodeError) as e:
        problems.append("%s: could not read manifest: %s: %s" % (manifest_path, type(e).__name__, e))
        return False, problems, notes, counts
    except ValueError as e:
        problems.append("%s: invalid manifest: %s" % (manifest_path, e))
        return False, problems, notes, counts
    listed = [entry for entry in listed if entry]
    counts["listed"] = len(listed)
    if not listed:
        problems.append("%s: manifest lists no files" % manifest_path)
    seen = set()
    for entry in listed:
        if entry in seen:
            notes.append("duplicate listed entry (checked once): %s" % entry)
            continue
        seen.add(entry)
        if _is_unsafe(entry):
            counts["missing"] += 1
            problems.append("%s: listed path escapes root or is absolute: %s" % (manifest_path, entry))
            continue
        full = os.path.join(root_abs, entry)
        if os.path.isfile(full):
            counts["present"] += 1
        else:
            counts["missing"] += 1
            problems.append("%s: listed file not found: %s" % (manifest_path, entry))
    manifest_abs = os.path.abspath(manifest_path)
    unlisted = []
    for dirpath, dirnames, filenames in os.walk(root_abs, followlinks=False):
        dirnames.sort()
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            if os.path.abspath(full) == manifest_abs:
                continue
            rel = os.path.relpath(full, root_abs).replace(os.sep, "/")
            if rel not in seen:
                unlisted.append(rel)
    counts["unlisted"] = len(unlisted)
    for rel in unlisted:
        msg = "%s: unlisted file: %s" % (manifest_path, rel)
        if allow_unlisted:
            notes.append(msg)
        else:
            problems.append(msg)
    return not problems, problems, notes, counts


def _fmt_counts(counts):
    return "listed: %d, present: %d, missing: %d, unlisted: %d" % (
        counts["listed"], counts["present"], counts["missing"], counts["unlisted"])


def main(argv):
    args = list(argv[1:])
    root = None
    allow_unlisted = False
    manifest = None
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--root" and i + 1 < len(args):
            root = args[i + 1]; i += 2
        elif arg.startswith("--root="):
            root = arg.split("=", 1)[1]; i += 1
        elif arg == "--allow-unlisted":
            allow_unlisted = True; i += 1
        elif arg in ("-h", "--help"):
            print(__doc__.strip()); return 0
        elif arg.startswith("--"):
            print("FAIL: unknown option %s" % arg); return 1
        elif manifest is None:
            manifest = arg; i += 1
        else:
            print("FAIL: unexpected extra argument %s" % arg); return 1
    if not manifest:
        print("FAIL: usage: python3 dataset_manifest_check.py MANIFEST [--root DIR] [--allow-unlisted]")
        return 1
    ok, problems, notes, counts = check(manifest, root=root, allow_unlisted=allow_unlisted)
    for note in notes:
        print("NOTE: " + note)
    if ok:
        print("PASS: %s (%s)" % (manifest, _fmt_counts(counts)))
        return 0
    for p in problems:
        print("FAIL: " + p)
    print("FAIL: %s (%s)" % (manifest, _fmt_counts(counts)))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
