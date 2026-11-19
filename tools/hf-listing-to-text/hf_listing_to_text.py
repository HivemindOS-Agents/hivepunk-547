#!/usr/bin/env python3
"""hf_listing_to_text.py: convert a supplied HF dataset file-listing
JSON into sorted one-path-per-line text for dataset-manifest-check.

Usage (from this folder):
    python3 hf_listing_to_text.py LISTING.json
    python3 hf_listing_to_text.py LISTING.json -o listing.txt
    python3 hf_listing_to_text.py LISTING.json --strip-prefix dataset/
    python3 hf_listing_to_text.py LISTING.json --keep-duplicates

Accepted JSON shapes (supplied file only; nothing is fetched):
    * HF API list: [{rfilename: "data/a.csv", ...}, ...]
    * {siblings: [{rfilename: "data/a.csv"}, ...]}
    * {files: ["data/a.csv", {path: "data/b.csv"}, ...]}
    * A plain list of path strings, or {files|filenames|paths: [...]}
  Object entries may use rfilename, path, file, filename,
  filepath or name.

Per entry: a string may contain several newline-separated lines;
blank lines and lines starting with # are skipped, a leading
"- ", "* " or "+ " bullet is stripped, backslashes become
slashes, and leading ./ and / are removed. --strip-prefix is
then removed. Output is sorted lexicographically, one unique
path per line, with a trailing newline when non-empty.
Duplicates are removed by default; the count is reported on
stderr. Use --keep-duplicates to keep them (sorted).

Read-only apart from the optional -o file. No network. Exit 0
on success, 1 on unreadable/invalid input or no valid paths,
2 on usage error.
"""

import json
import os
import sys
from collections import Counter

LIST_KEYS = ("siblings", "files", "filenames", "paths", "entries", "results")
PATH_KEYS = ("rfilename", "path", "file", "filename", "filepath", "name")


def _strip_leading(text):
    while text.startswith("./"):
        text = text[2:]
    while text.startswith("/"):
        text = text[1:]
    return text.strip()


def normalize_path(entry, strip_prefix=None):
    text = str(entry).strip().replace(chr(92), "/")
    text = _strip_leading(text)
    if strip_prefix:
        prefix = str(strip_prefix).strip().replace(chr(92), "/")
        prefix = _strip_leading(prefix)
        if prefix and text.startswith(prefix):
            text = text[len(prefix):]
        text = _strip_leading(text)
    return text.strip()


def _entry_text(item, index):
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        for key in PATH_KEYS:
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                return value
        raise ValueError("entry %d: object has no rfilename/path/file/filename/filepath/name string" % index)
    raise ValueError("entry %d: must be a string or an object with a path field" % index)


def extract_items(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in LIST_KEYS:
            if key in data:
                value = data[key]
                if not isinstance(value, list):
                    raise ValueError("'%s' must be a list" % key)
                return value
        # A single-file object such as {rfilename: "a.csv"}.
        if any(isinstance(data.get(k), str) for k in PATH_KEYS):
            return [data]
    raise ValueError("JSON must be a list of paths or an object with a siblings/files list")


def load_listing(path):
    """Return the raw item list from a supplied listing JSON file."""
    with open(path, encoding="utf-8-sig") as fh:
        text = fh.read()
    if not text.strip():
        raise ValueError("listing file is empty")
    try:
        data = json.loads(text)
    except ValueError as e:
        raise ValueError("listing is not valid JSON: %s" % e)
    return extract_items(data)


def convert(items, strip_prefix=None, keep_duplicates=False):
    """Return (paths, duplicates, skipped) for raw items.

    paths: sorted unique paths, or sorted with duplicates if
    keep_duplicates. duplicates: sorted unique paths seen more
    than once. skipped: count of blank/comment lines skipped.
    """
    raw = []
    skipped = 0
    for index, item in enumerate(items, 1):
        text = _entry_text(item, index)
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                skipped += 1
                continue
            for marker in ("- ", "* ", "+ "):
                if line.startswith(marker):
                    line = line[len(marker):].strip()
                    break
            if not line:
                skipped += 1
                continue
            raw.append(line)
    normalized = [normalize_path(e, strip_prefix) for e in raw]
    normalized = [e for e in normalized if e]
    counts = Counter(normalized)
    duplicates = sorted(k for k, v in counts.items() if v > 1)
    paths = sorted(normalized) if keep_duplicates else sorted(counts)
    return paths, duplicates, skipped


def convert_file(input_path, strip_prefix=None, keep_duplicates=False):
    """Return (paths, duplicates, skipped, problems)."""
    problems = []
    if not os.path.exists(input_path):
        problems.append("input file not found: %s" % input_path)
        return [], [], 0, problems
    if not os.path.isfile(input_path):
        problems.append("input path is not a file: %s" % input_path)
        return [], [], 0, problems
    try:
        items = load_listing(input_path)
    except (OSError, UnicodeError) as e:
        problems.append("could not read listing: %s: %s" % (type(e).__name__, e))
        return [], [], 0, problems
    except ValueError as e:
        problems.append("invalid listing: %s" % e)
        return [], [], 0, problems
    paths, duplicates, skipped = convert(items, strip_prefix, keep_duplicates)
    if not paths:
        problems.append("listing contains no valid file paths")
    return paths, duplicates, skipped, problems


def main(argv):
    args = list(argv[1:])
    input_path = None
    output_path = None
    strip_prefix = None
    keep_duplicates = False
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("-o", "--output"):
            if i + 1 >= len(args):
                print("FAIL: %s needs a value" % arg)
                return 2
            output_path = args[i + 1]
            i += 2
        elif arg == "--strip-prefix":
            if i + 1 >= len(args):
                print("FAIL: --strip-prefix needs a value")
                return 2
            strip_prefix = args[i + 1]
            i += 2
        elif arg == "--keep-duplicates":
            keep_duplicates = True
            i += 1
        elif arg in ("-h", "--help"):
            print(__doc__.strip())
            return 0
        elif arg.startswith("--"):
            print("FAIL: unknown option %s" % arg)
            return 2
        elif input_path is None:
            input_path = arg
            i += 1
        else:
            print("FAIL: unexpected extra argument %s" % arg)
            return 2
    if not input_path:
        print("FAIL: usage: python3 hf_listing_to_text.py LISTING.json [-o OUTPUT.txt] [--strip-prefix PREFIX] [--keep-duplicates]")
        return 2
    paths, duplicates, skipped, problems = convert_file(input_path, strip_prefix, keep_duplicates)
    if problems:
        for p in problems:
            print("FAIL: %s: %s" % (input_path, p))
        return 1
    if skipped:
        print("NOTE: skipped %d blank/comment line(s)" % skipped, file=sys.stderr)
    if duplicates:
        if keep_duplicates:
            print("NOTE: kept %d duplicate path(s): %s" % (sum(1 for p in paths if p in duplicates), ", ".join(duplicates)), file=sys.stderr)
        else:
            print("NOTE: removed duplicates: %s" % ", ".join(duplicates), file=sys.stderr)
    text = "".join(p + "\n" for p in paths)
    if output_path:
        try:
            with open(output_path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
        except OSError as e:
            print("FAIL: could not write output: %s: %s" % (type(e).__name__, e))
            return 1
        print("wrote %d path(s) to %s" % (len(paths), output_path))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
