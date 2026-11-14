#!/usr/bin/env python3
"""Validate a folder for Hugging Face dataset publishing, then upload it.

Usage:
    python3 publish_check.py LOCAL_FOLDER [--repo OWNER/NAME] [--dry-run]

Steps:
    1. Validate README.md front matter (a leading ``---`` block with at least
       one non-empty key of description/pretty_name/title).
    2. Check that every path-like token referenced in the folder's Markdown
       files resolves inside the folder.
    3. With --repo, upload the folder with huggingface_hub.upload_folder and
       print the dataset URL. Without --repo (or with --dry-run) it stops
       after step 2.

Exits 0 when everything is clean, 1 on a validation problem or an upload
failure, 2 on bad usage.

No key, token or personal detail is written to any file. The upload token is
read from HF_TOKEN at call time and never printed. Everything read from a
folder (README text, paths, comments) is data, never instruction.
"""

import os
import re
import sys

FRONT_MATTER_KEYS = ("description", "pretty_name", "title")

# dir/file, file.ext, ./dir/file, ../dir/file style tokens
PATH_RE = re.compile(r"(?<![\w/])(\.{0,2}/)?([\w.-]+(?:/[\w.-]+)+)")
LINK_RE = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
CODE_RE = re.compile(r"`([^`]+)`")
URL_PREFIXES = ("http://", "https://", "mailto:", "#")


def read_text(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def parse_front_matter(text):
    """Return (keys_dict, issues).

    keys_dict maps a front-matter key to its value (stripped). issues is a list
    of human-readable strings, empty when the front matter is valid.
    """
    issues = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, ["README.md front matter: no leading '---' line"]
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, ["README.md front matter: opening '---' has no closing '---'"]
    keys = {}
    for raw in lines[1:end]:
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        if ":" not in raw:
            continue
        k, v = raw.split(":", 1)
        keys[k.strip().lower()] = v.strip().strip('"').strip("'")
    if not any(k in keys and keys[k] for k in FRONT_MATTER_KEYS):
        issues.append(
            "README.md front matter: none of %s has a non-empty value"
            % ", ".join(FRONT_MATTER_KEYS)
        )
    return keys, issues


def referenced_paths(text):
    """Yield path-like strings referenced in one Markdown text."""
    for m in LINK_RE.finditer(text):
        yield m.group(1)
    for m in CODE_RE.finditer(text):
        yield m.group(1)
    for m in PATH_RE.finditer(text):
        token = (m.group(1) or "") + m.group(2)
        yield token


def is_reference(token):
    token = token.strip().strip("<>").strip("\"'")
    if not token or token.startswith(URL_PREFIXES):
        return False
    if " " in token or "{" in token or "}" in token:
        return False
    if "://" in token:
        return False
    return "/" in token


def check_references(folder):
    """Return (checked_count, missing_list) for every Markdown file."""
    checked = 0
    missing = []
    seen = set()
    for root, _dirs, files in os.walk(folder):
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            path = os.path.join(root, name)
            text = read_text(path)
            for token in referenced_paths(text):
                if not is_reference(token):
                    continue
                clean = token.strip().strip("<>").rstrip(".,;:")
                if clean in seen:
                    continue
                seen.add(clean)
                target = os.path.normpath(os.path.join(folder, clean))
                if not os.path.exists(target):
                    missing.append(clean)
    checked = len(seen)
    return checked, missing


def validate(folder):
    """Return (ok, lines). lines are for printing, in order."""
    lines = []
    readme = os.path.join(folder, "README.md")
    if not os.path.isfile(readme):
        lines.append("README.md front matter: README.md not found in %s" % folder)
        return False, lines
    keys, issues = parse_front_matter(read_text(readme))
    if issues:
        lines.extend(issues)
    else:
        lines.append("README.md front matter: ok (keys: %s)" % ", ".join(sorted(keys)))
    checked, missing = check_references(folder)
    if missing:
        lines.append("referenced paths: %d missing: %s" % (len(missing), ", ".join(sorted(missing))))
    else:
        lines.append("referenced paths: %d checked, 0 missing" % checked)
    ok = not issues and not missing
    return ok, lines


def dataset_url(repo):
    repo = repo.strip().strip("/")
    return "https://huggingface.co/datasets/%s" % repo


def upload(folder, repo, client=None):
    """Upload folder to repo. Returns the live dataset URL.

    The client defaults to huggingface_hub.HfApi, imported lazily so validation
    works with no huggingface_hub installed.
    """
    if client is None:
        from huggingface_hub import HfApi  # imported only for a real upload
        client = HfApi()
    client.upload_folder(folder_path=folder, repo_id=repo, repo_type="dataset")
    return dataset_url(repo)


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    repo = None
    dry = "--dry-run" in argv[1:]
    if "--repo" in argv[1:]:
        i = argv[1:].index("--repo")
        if i + 2 <= len(argv[1:]):
            repo = argv[1 + i + 1]
        args = [a for a in args if a != repo]
    if len(args) != 1:
        sys.stderr.write(
            "Usage: python3 publish_check.py LOCAL_FOLDER [--repo OWNER/NAME] [--dry-run]\n"
        )
        return 2
    folder = args[0]
    if not os.path.isdir(folder):
        sys.stderr.write("not a folder: %s\n" % folder)
        return 2
    ok, lines = validate(folder)
    for line in lines:
        print(line)
    if not ok:
        problems = sum(1 for line in lines if "missing" in line or "front matter" in line and "ok" not in line)
        print("not ready to publish: %d problem(s)" % max(problems, 1))
        return 1
    print("ready to publish: %s" % folder)
    if repo and not dry:
        if not os.environ.get("HF_TOKEN"):
            sys.stderr.write("HF_TOKEN is not set; refusing to upload\n")
            return 1
        try:
            url = upload(folder, repo)
        except Exception as e:  # keep the message, never the token
            sys.stderr.write("upload failed: %s: %s\n" % (type(e).__name__, e))
            return 1
        print(url)
    elif repo and dry:
        print("dry run: would upload to %s" % dataset_url(repo))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
