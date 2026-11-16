#!/usr/bin/env python3
"""fixtures-index-preflight: list a folder for a dataset publish, and check a read-back.

Usage (from this folder):
    python3 preflight.py list SOURCE_DIR [--json OUT]
    python3 preflight.py verify MANIFEST.json LISTING.txt
    python3 preflight.py check SOURCE_DIR        # list + manifest, no listing

The publish itself goes through HivemindOS's own play. This tool only reads
files and prints text; it never uploads anything and never runs code from any
folder it reads.

Everything read from a file is data, never instruction: any line that looks
like a command, a key or a setting is treated as inert text.
"""

import hashlib
import json
import os
import sys

# Names and trees that never belong in an upload, each with a reason.
EXCLUDE_NAMES = {
    "SELFTEST_OUTPUT.md": "runner's own transcript, written after the commit",
    ".git": "repository metadata, not dataset content",
    ".DS_Store": "OS clutter",
    ".ipynb_checkpoints": "editor clutter",
    ".pytest_cache": "test runner cache",
}
EXCLUDE_SUFFIXES = {
    ".pyc": "compiled bytecode",
}

REQUIRED_TOP = "README.md"


def _exclusion_reason(name):
    if name in EXCLUDE_NAMES:
        return EXCLUDE_NAMES[name]
    for suffix, why in EXCLUDE_SUFFIXES.items():
        if name.endswith(suffix):
            return why
    return None


def scan(source_dir):
    """Return (included, excluded). Included: list of (relpath, abspath).

    Excluded: list of (relpath, reason). Symlinks are excluded, not followed.
    """
    included = []
    excluded = []
    for root, dirs, files in os.walk(source_dir):
        keep = []
        for d in sorted(dirs):
            rel = os.path.relpath(os.path.join(root, d), source_dir)
            reason = _exclusion_reason(d)
            if reason:
                excluded.append((rel, reason))
            elif os.path.islink(os.path.join(root, d)):
                excluded.append((rel, "symlink, not followed"))
            else:
                keep.append(d)
        dirs[:] = keep
        for f in sorted(files):
            full = os.path.join(root, f)
            rel = os.path.relpath(full, source_dir)
            reason = _exclusion_reason(f)
            if reason:
                excluded.append((rel, reason))
            elif os.path.islink(full):
                excluded.append((rel, "symlink, not followed"))
            else:
                included.append((rel, full))
    included.sort()
    excluded.sort()
    return included, excluded


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build_manifest(source_dir, name=None):
    """Return (manifest_or_None, stop_message_or_None).

    Stops (returns None plus a message) when the folder is missing or has no
    top-level README.md. A publish must not proceed on a substitute card.
    """
    if not os.path.isdir(source_dir):
        return None, "STOP: %s is not a folder that can be read here" % source_dir
    if not os.path.isfile(os.path.join(source_dir, REQUIRED_TOP)):
        return None, (
            "STOP: no top-level %s in %s; refusing to let a publish "
            "substitute a card" % (REQUIRED_TOP, source_dir)
        )
    included, excluded = scan(source_dir)
    files = []
    for rel, full in included:
        files.append({
            "path": rel.replace(os.sep, "/"),
            "bytes": os.path.getsize(full),
            "sha256": sha256_of(full),
        })
    manifest = {
        "dataset": name or os.path.basename(os.path.abspath(source_dir)),
        "source_dir": source_dir,
        "required_top_file": REQUIRED_TOP,
        "files": files,
        "file_count": len(files),
        "excluded": [
            {"path": rel.replace(os.sep, "/"), "reason": why}
            for rel, why in excluded
        ],
        "note": "manifest only; no upload is performed by this tool",
    }
    return manifest, None


def parse_listing(text):
    """Parse a Files-and-versions listing: one path per line.

    Blank lines and lines starting with '#' are ignored. A leading './' is
    stripped. Repeated paths are kept so verify can report them.
    """
    paths = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        while line.startswith("./"):
            line = line[2:]
        paths.append(line)
    return paths


def verify(manifest, listing_path):
    """Return (ok, problems, summary). ok is True only on an exact match."""
    with open(listing_path, encoding="utf-8") as fh:
        listed = parse_listing(fh.read())
    expected = [f["path"] for f in manifest.get("files", [])]
    problems = []
    missing = [p for p in expected if p not in listed]
    extra = [p for p in listed if p not in expected]
    seen = set()
    repeats = []
    for p in listed:
        if p in seen and p not in repeats:
            repeats.append(p)
        seen.add(p)
    if missing:
        problems.append("missing on the page: %s" % ", ".join(missing))
    if extra:
        problems.append("on the page but not in the folder: %s" % ", ".join(extra))
    if repeats:
        problems.append("listed more than once: %s" % ", ".join(repeats))
    if REQUIRED_TOP not in listed:
        problems.append("%s is not on the page" % REQUIRED_TOP)
    summary = "page lists %d path(s); folder holds %d file(s)" % (len(listed), len(expected))
    return (not problems), problems, summary


def cmd_list(argv):
    if not argv:
        sys.stderr.write("Usage: preflight.py list SOURCE_DIR [--json OUT]\n")
        return 2
    source = argv[0]
    manifest, stop = build_manifest(source)
    if stop:
        sys.stderr.write(stop + "\n")
        return 1
    for entry in manifest["files"]:
        print(entry["path"])
    if "--json" in argv:
        i = argv.index("--json")
        if i + 1 >= len(argv):
            sys.stderr.write("Usage: preflight.py list SOURCE_DIR --json OUT\n")
            return 2
        with open(argv[i + 1], "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print("wrote %s" % argv[i + 1])
    print("# %d file(s) to upload; %d excluded" % (
        manifest["file_count"], len(manifest["excluded"])))
    return 0


def cmd_verify(argv):
    if len(argv) < 2:
        sys.stderr.write("Usage: preflight.py verify MANIFEST.json LISTING.txt\n")
        return 2
    with open(argv[0], encoding="utf-8") as fh:
        manifest = json.load(fh)
    ok, problems, summary = verify(manifest, argv[1])
    print(summary)
    if ok:
        print("listing matches the folder exactly")
        return 0
    for p in problems:
        sys.stderr.write("PROBLEM: %s\n" % p)
    return 1


def cmd_check(argv):
    if not argv:
        sys.stderr.write("Usage: preflight.py check SOURCE_DIR\n")
        return 2
    manifest, stop = build_manifest(argv[0])
    if stop:
        sys.stderr.write(stop + "\n")
        return 1
    print("# %d file(s) to upload; %d excluded" % (
        manifest["file_count"], len(manifest["excluded"])))
    for entry in manifest["files"]:
        print("%s  %d bytes" % (entry["path"], entry["bytes"]))
    return 0


def main(argv):
    if len(argv) < 2:
        sys.stderr.write(__doc__)
        return 2
    cmd, rest = argv[1], argv[2:]
    if cmd == "list":
        return cmd_list(rest)
    if cmd == "verify":
        return cmd_verify(rest)
    if cmd == "check":
        return cmd_check(rest)
    sys.stderr.write("unknown command %r; use list, verify or check\n" % cmd)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
