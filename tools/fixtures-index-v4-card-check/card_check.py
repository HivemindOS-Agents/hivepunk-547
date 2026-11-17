#!/usr/bin/env python3
"""card_check.py: validate a Hugging Face dataset-card README against data.csv.

Usage (from this folder):
    python3 card_check.py
    python3 card_check.py README.md data.csv
    python3 card_check.py README.md data.csv fixtures-index-v4
    python3 card_check.py --check README.md data.csv fixtures-index-v4

Checks, reading files only as data (no network, no publish):
  1. README starts with YAML-style frontmatter delimited by --- lines.
  2. Frontmatter has non-empty license, non-empty language, and a
     non-empty tags list (inline [a, b] or following - item lines).
  3. Dataset name appears as an exact level-1 heading in the body:
     "# <dataset_name>".
  4. data.csv has a file_name column with unique, non-empty values.
  5. A "## Files" (or "## File list") section lists exactly those
     file_name values as bullets, no missing, extra, or duplicate.

Exit 0 and print "ok: ..." when all checks pass; exit 1 with FAIL lines
otherwise. Defaults: README.md, data.csv, fixtures-index-v4 beside this file.
"""

import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_README = os.path.join(HERE, "README.md")
DEFAULT_CSV = os.path.join(HERE, "data.csv")
DEFAULT_NAME = "fixtures-index-v4"
REQUIRED_KEYS = ["license", "language", "tags"]


def _parse_inline_list(value):
    inner = value[1:-1].strip()
    return [p.strip().strip("'\"") for p in inner.split(",") if p.strip()] if inner else []


def parse_frontmatter(text):
    """Return (meta, body, problems). meta values are str or list for tags."""
    problems = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text, ["README does not start with a '---' frontmatter delimiter"]
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text, ["frontmatter has no closing '---' delimiter"]
    meta = {}
    current = None
    for raw in lines[1:end]:
        line = raw.rstrip()
        if not line.strip():
            continue
        bullet = re.match(r"^\s*-\s+(.+\S)\s*$", line)
        if bullet and current == "tags":
            existing = meta.get("tags")
            if not isinstance(existing, list):
                existing = [existing] if existing else []
                meta["tags"] = existing
            existing.append(bullet.group(1).strip().strip("'\""))
            continue
        stripped = line.strip()
        if current == "tags" and stripped.startswith("[") and stripped.endswith("]"):
            meta["tags"] = _parse_inline_list(stripped)
            continue
        m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", line)
        if not m:
            problems.append("unparseable frontmatter line: %r" % raw)
            continue
        key, value = m.group(1).strip(), m.group(2).strip()
        current = key
        if key == "tags" and value.startswith("[") and value.endswith("]"):
            meta["tags"] = _parse_inline_list(value)
        elif key == "tags" and value:
            meta["tags"] = [value]
        elif key == "tags":
            meta["tags"] = []
        else:
            meta[key] = value.strip("'\"")
    body = "\n".join(lines[end + 1:])
    return meta, body, problems


def check_frontmatter(meta):
    problems = []
    for key in REQUIRED_KEYS:
        if key not in meta:
            problems.append("frontmatter missing required key: %s" % key)
    if "license" in meta and not str(meta["license"]).strip():
        problems.append("frontmatter license is empty")
    if "language" in meta and not str(meta["language"]).strip():
        problems.append("frontmatter language is empty")
    if "tags" in meta:
        tags = meta["tags"] if isinstance(meta["tags"], list) else [meta["tags"]]
        if not [t for t in tags if str(t).strip()]:
            problems.append("frontmatter tags is empty")
    return problems


def check_dataset_name(body, dataset_name):
    for line in body.splitlines():
        if re.match(r"^#\s+" + re.escape(dataset_name) + r"\s*$", line.strip()):
            return []
    return ["dataset name %r not found as an exact '# %s' heading" % (dataset_name, dataset_name)]


def extract_file_list(body):
    """Return (files, found_section)."""
    files = []
    in_section = False
    found = False
    for line in body.splitlines():
        heading = re.match(r"^##\s+(.+?)\s*$", line.strip())
        if heading:
            in_section = heading.group(1).strip().lower() in ("files", "file list")
            if in_section:
                found = True
            continue
        if in_section:
            m = re.match(r"^\s*[-*]\s+`?([^`\s]+)`?\s*$", line)
            if m:
                files.append(m.group(1).strip())
    return files, found


def read_csv_names(path):
    if not os.path.isfile(path):
        return [], ["file not found: %s" % path]
    try:
        with open(path, encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames is None or "file_name" not in reader.fieldnames:
                return [], ["data.csv has no file_name column (header %r)" % (reader.fieldnames,)]
            names = [(r.get("file_name") or "").strip() for r in reader]
    except (OSError, csv.Error, UnicodeError) as e:
        return [], ["could not read %s: %s: %s" % (path, type(e).__name__, e)]
    problems = []
    if any(not n for n in names):
        problems.append("data.csv has an empty file_name")
    if len(set(names)) != len(names):
        dupes = sorted({n for n in names if names.count(n) > 1})
        problems.append("data.csv duplicate file_name(s): %s" % ", ".join(dupes))
    return names, problems


def check_file_list(listed, csv_names):
    problems = []
    if len(set(listed)) != len(listed):
        dupes = sorted({n for n in listed if listed.count(n) > 1})
        problems.append("file list duplicate(s): %s" % ", ".join(dupes))
    missing = [n for n in csv_names if n not in listed]
    extra = [n for n in listed if n not in csv_names]
    if missing:
        problems.append("file list missing from card: %s" % ", ".join(missing))
    if extra:
        problems.append("file list has extra names not in data.csv: %s" % ", ".join(extra))
    return problems


def verify(readme_path, csv_path, dataset_name=DEFAULT_NAME):
    """Return (ok, problems, listed_files)."""
    if not os.path.isfile(readme_path):
        return False, ["file not found: %s" % readme_path], []
    try:
        with open(readme_path, encoding="utf-8") as fh:
            text = fh.read()
    except (OSError, UnicodeError) as e:
        return False, ["could not read %s: %s: %s" % (readme_path, type(e).__name__, e)], []
    meta, body, problems = parse_frontmatter(text)
    problems += check_frontmatter(meta)
    problems += check_dataset_name(body, dataset_name)
    listed, found = extract_file_list(body)
    if not found:
        problems.append("no '## Files' or '## File list' section in README")
    csv_names, csv_problems = read_csv_names(csv_path)
    problems += csv_problems
    if csv_names:
        problems += check_file_list(listed, csv_names)
    return (not problems), problems, listed


def main(argv):
    args = [a for a in argv[1:] if a != "--check"]
    readme = os.path.abspath(args[0]) if len(args) > 0 else DEFAULT_README
    csv_path = os.path.abspath(args[1]) if len(args) > 1 else DEFAULT_CSV
    name = args[2] if len(args) > 2 else DEFAULT_NAME
    ok, problems, listed = verify(readme, csv_path, name)
    if ok:
        print("ok: %s card for %r has license/language/tags and Files list "
              "matching data.csv (%s)" % (readme, name, ", ".join(listed)))
        return 0
    for p in problems:
        print("FAIL: " + p)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
