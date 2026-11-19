#!/usr/bin/env python3
"""dataset_manifest_check.py: compare a dataset manifest JSON file list
against a supplied public file-listing text file.

Usage (from this folder):
    python3 dataset_manifest_check.py MANIFEST.json LISTING.txt
    python3 dataset_manifest_check.py MANIFEST.json LISTING.txt --strip-prefix dataset/

Manifest JSON (.json): a list of path strings, or an object with a
"files" list whose entries are strings or objects with a
path/file/filename/name field.

Listing text (.txt/.md/.tsv/extensionless): one path per line; blank
lines and # comment lines are ignored and a leading "- ", "* " or
"+ " bullet marker is stripped. The listing is supplied by the
caller (for example text copied from a public file listing); this
tool never fetches it.

Normalisation (applied to both sides): strip whitespace, convert
backslashes to slashes, repeatedly remove a leading "./", remove a
leading "/", and remove --strip-prefix when present. No other
rewriting is done, so comparison is of exact normalised sets.

Result: PASS only when the two unique sets are equal and neither
side has duplicates. Otherwise FAIL. Prints counts and sorted
differences. Read-only, no network, writes nothing. Exit 0 on PASS,
1 on FAIL/unreadable input, 2 on usage error.
"""

import json
import os
import sys
from collections import Counter

FIELDS = ("path", "file", "filename", "name")


def _strip_leading(text):
    while text.startswith("./"):
        text = text[2:]
    while text.startswith("/"):
        text = text[1:]
    return text.strip()


def normalize(entry, strip_prefix=None):
    if not isinstance(entry, str):
        raise ValueError("file entry must be a string, got %r" % (entry,))
    text = entry.strip().replace("\\", "/")
    # Strip ./ and / BEFORE the prefix, so ./dataset/a.csv is
    # recognised as starting with dataset/ just like dataset/a.csv.
    text = _strip_leading(text)
    if strip_prefix:
        prefix = str(strip_prefix).strip().replace("\\", "/")
        prefix = _strip_leading(prefix)
        if prefix and text.startswith(prefix):
            text = text[len(prefix):]
        text = _strip_leading(text)
    return text.strip()


def load_manifest(path):
    """Return raw entry list from a manifest JSON file."""
    with open(path, encoding="utf-8-sig") as fh:
        text = fh.read()
    if not text.strip():
        raise ValueError("manifest file is empty")
    try:
        data = json.loads(text)
    except ValueError as e:
        raise ValueError("manifest is not valid JSON: %s" % e)
    items = None
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict) and isinstance(data.get("files"), list):
        items = data["files"]
    if items is None:
        raise ValueError("manifest JSON must be a list of paths or an object with a 'files' list")
    out = []
    for i, item in enumerate(items, 1):
        if isinstance(item, str):
            out.append(item)
        elif isinstance(item, dict):
            value = None
            for key in FIELDS:
                if isinstance(item.get(key), str) and item.get(key).strip():
                    value = item[key]
                    break
            if value is None:
                raise ValueError("manifest entry %d has no path/file/filename/name string" % i)
            out.append(value)
        else:
            raise ValueError("manifest entry %d must be a string or an object with a path field" % i)
    return out


def load_listing(path):
    """Return raw entry list from a plain-text file listing."""
    with open(path, encoding="utf-8-sig") as fh:
        lines = fh.read().splitlines()
    out = []
    for line in lines:
        text = line.strip()
        if not text or text.startswith("#"):
            continue
        for marker in ("- ", "* ", "+ "):
            if text.startswith(marker):
                text = text[len(marker):].strip()
                break
        if text:
            out.append(text)
    return out


def _duplicates(entries):
    counts = Counter(entries)
    return sorted(k for k, v in counts.items() if v > 1)


def compare(manifest_entries, listing_entries, strip_prefix=None):
    """Compare two raw entry lists. Returns a result dict."""
    manifest = [normalize(e, strip_prefix) for e in manifest_entries]
    listing = [normalize(e, strip_prefix) for e in listing_entries]
    manifest = [e for e in manifest if e]
    listing = [e for e in listing if e]
    m_set, l_set = set(manifest), set(listing)
    result = {
        "manifest_count": len(m_set),
        "listing_count": len(l_set),
        "manifest_total": len(manifest),
        "listing_total": len(listing),
        "common": len(m_set & l_set),
        "only_in_manifest": sorted(m_set - l_set),
        "only_in_listing": sorted(l_set - m_set),
        "duplicates_in_manifest": _duplicates(manifest),
        "duplicates_in_listing": _duplicates(listing),
    }
    result["ok"] = (
        not result["only_in_manifest"]
        and not result["only_in_listing"]
        and not result["duplicates_in_manifest"]
        and not result["duplicates_in_listing"]
    )
    return result


def check(manifest_path, listing_path, strip_prefix=None):
    """Return (ok, result_or_None, problems, notes)."""
    problems = []
    notes = []
    for label, path in (("manifest", manifest_path), ("listing", listing_path)):
        if not os.path.exists(path):
            problems.append("%s: %s file not found: %s" % (manifest_path, label, path))
        elif not os.path.isfile(path):
            problems.append("%s: %s path is not a file: %s" % (manifest_path, label, path))
    if problems:
        return False, None, problems, notes
    try:
        manifest_entries = load_manifest(manifest_path)
    except (OSError, UnicodeError) as e:
        problems.append("%s: could not read manifest: %s: %s" % (manifest_path, type(e).__name__, e))
        return False, None, problems, notes
    except ValueError as e:
        problems.append("%s: invalid manifest: %s" % (manifest_path, e))
        return False, None, problems, notes
    try:
        listing_entries = load_listing(listing_path)
    except (OSError, UnicodeError) as e:
        problems.append("%s: could not read listing: %s: %s" % (manifest_path, type(e).__name__, e))
        return False, None, problems, notes
    if not manifest_entries:
        problems.append("%s: manifest lists no files" % manifest_path)
    if not listing_entries:
        problems.append("%s: listing contains no files: %s" % (listing_path, listing_path))
    if problems:
        return False, None, problems, notes
    result = compare(manifest_entries, listing_entries, strip_prefix=strip_prefix)
    if strip_prefix:
        notes.append("stripped prefix %r from both sides" % strip_prefix)
    return result["ok"], result, problems, notes


def _summary(result):
    return "manifest: %d, listing: %d, common: %d, only_in_manifest: %d, only_in_listing: %d, duplicates_manifest: %d, duplicates_listing: %d" % (
        result["manifest_count"], result["listing_count"], result["common"],
        len(result["only_in_manifest"]), len(result["only_in_listing"]),
        len(result["duplicates_in_manifest"]), len(result["duplicates_in_listing"]))


def main(argv):
    args = list(argv[1:])
    strip_prefix = None
    positional = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--strip-prefix":
            if i + 1 >= len(args):
                print("FAIL: --strip-prefix needs a value")
                return 2
            strip_prefix = args[i + 1]
            i += 2
        elif arg in ("-h", "--help"):
            print(__doc__.strip())
            return 0
        elif arg.startswith("--"):
            print("FAIL: unknown option %s" % arg)
            return 2
        else:
            positional.append(arg)
            i += 1
    if len(positional) != 2:
        print("FAIL: usage: python3 dataset_manifest_check.py MANIFEST.json LISTING.txt [--strip-prefix PREFIX]")
        return 2
    manifest_path, listing_path = positional
    ok, result, problems, notes = check(manifest_path, listing_path, strip_prefix=strip_prefix)
    for note in notes:
        print("NOTE: " + note)
    if result is None:
        for p in problems:
            print("FAIL: " + p)
        print("FAIL: %s vs %s" % (manifest_path, listing_path))
        return 1
    if ok:
        print("PASS: %s vs %s (%s)" % (manifest_path, listing_path, _summary(result)))
        return 0
    for entry in result["only_in_manifest"]:
        print("FAIL: only in manifest: %s" % entry)
    for entry in result["only_in_listing"]:
        print("FAIL: only in listing: %s" % entry)
    for entry in result["duplicates_in_manifest"]:
        print("FAIL: duplicate in manifest: %s" % entry)
    for entry in result["duplicates_in_listing"]:
        print("FAIL: duplicate in listing: %s" % entry)
    print("FAIL: %s vs %s (%s)" % (manifest_path, listing_path, _summary(result)))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
