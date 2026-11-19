#!/usr/bin/env python3
"""dataset_card_licence.py: add/check a YAML licence tag on an HF dataset card.

Usage (from this folder):
    python3 dataset_card_licence.py existing_README.md --license mit
    python3 dataset_card_licence.py existing_README.md --license mit -o README.md
    python3 dataset_card_licence.py existing_README.md --check-only
    python3 dataset_card_licence.py existing_README.md --license apache-2.0 --force
    python3 dataset_card_licence.py existing_README.md --license mit --title "stated-facts-check"

Reads a supplied dataset card (existing README.md), parses its YAML
front matter between --- lines, checks the fields, and prints a
ready-to-republish card to stdout (or -o file) with a `license:`
key in the front matter. Hugging Face uses the US spelling
`license:` even when the tool name says "licence".

Checks reported as problems (exit 1 unless fixed by the options):
  - no front matter / no license field and no --license given
  - license value not in the known HF/SPDX set below
  - existing license differs from --license and --force is absent
  - `licence:` (British spelling) used instead of `license:`
  - no Markdown title (# ...) in the body
  - empty or missing body text

Unknown front-matter fields and the whole body are preserved
verbatim. Missing known fields are not invented except `license`
(and title if --title is given and no title exists).

Read-only on the input, no network. Exit 0 OK, 1 card problem or
bad input, 2 usage error.
"""

import os
import re
import sys

KNOWN_LICENSES = (
    "mit", "apache-2.0", "cc-by-4.0", "cc-by-sa-4.0", "cc-by-nc-4.0",
    "cc-by-nd-4.0", "cc0-1.0", "gpl-3.0", "lgpl-3.0", "agpl-3.0",
    "bsd-3-clause", "bsd-2-clause", "unlicense", "other", "unknown",
    "artistic-2.0", "mpl-2.0", "epl-2.0", "isc", "zlib",
)
TITLE_RE = re.compile(r"^#\s+\S", re.M)
KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")


def normalise_license(value):
    return str(value or "").strip().strip("'\"").lower().replace("_", "-")


def is_known_license(value):
    return normalise_license(value) in KNOWN_LICENSES


def parse_card(text):
    """Return (fields list of [key, value], body, problems)."""
    problems = []
    text = text.replace("\r\n", "\n")
    fields = []
    body = text
    if text.startswith("---"):
        lines = text.split("\n")
        end = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end = i
                break
        if end is None:
            problems.append("front matter opened with --- but never closed")
        else:
            current = None
            for line in lines[1:end]:
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                m = KEY_RE.match(line)
                if m:
                    current = [m.group(1).strip(), m.group(2).strip()]
                    fields.append(current)
                elif current is not None and line.strip().startswith("-") and (len(line.strip()) == 1 or line.strip()[1:2] in (" ", "\t")):
                    # YAML block list item under the current key, indented
                    # or not (e.g. "tags:\n- csv" or "license:\n- mit");
                    # keep the item inline on that key's value.
                    item = line.strip()[1:].strip()
                    if current[1]:
                        current[1] = current[1] + ", " + item if item else current[1]
                    else:
                        current[1] = item
                else:
                    problems.append("unparsed front-matter line: %r" % line)
            body = "\n".join(lines[end + 1:])
    return fields, body, problems


def get_field(fields, name):
    for key, value in fields:
        if key == name:
            return value
    return None


def set_field(fields, name, value):
    for pair in fields:
        if pair[0] == name:
            pair[1] = value
            return
    fields.append([name, value])


def check_fields(fields, body):
    """Return list of problem strings (empty when the card is fine)."""
    problems = []
    keys = [k for k, _ in fields]
    if "licence" in keys:
        problems.append("`licence:` spelling in front matter; Hugging Face expects `license:`")
    lic = get_field(fields, "license")
    if lic is None or not str(lic).strip():
        problems.append("missing license field in front matter")
    elif not is_known_license(lic):
        problems.append("unknown license value %r (known: %s)" % (lic, ", ".join(KNOWN_LICENSES)))
    if not TITLE_RE.search(body or ""):
        problems.append("no Markdown title (# ...) in card body")
    if not (body or "").strip():
        problems.append("empty card body")
    return problems


def render_card(fields, body):
    body = (body or "").strip("\n")
    out = ["---"]
    for key, value in fields:
        out.append("%s: %s" % (key, value) if str(value) != "" else "%s:" % key)
    out.append("---")
    out.append("")
    if body:
        out.append(body)
    else:
        out.append("# Dataset")
        out.append("")
        out.append("TODO: describe this dataset, its fields and how it was compiled.")
    return "\n".join(out).rstrip("\n") + "\n"


def build_card(text, license_value=None, force=False, title=None):
    """Return (card_text_or_None, problems). Fixes what options allow."""
    fields, body, problems = parse_card(text or "")
    # British spelling: drop it once license is known, keep its value.
    lic = get_field(fields, "license")
    brit = get_field(fields, "licence")
    if brit is not None:
        if lic is None:
            lic = brit
        fields[:] = [p for p in fields if p[0] != "licence"]
    if license_value:
        lic_norm = normalise_license(license_value)
        if not is_known_license(lic_norm):
            problems.append("unknown license value %r (known: %s)" % (license_value, ", ".join(KNOWN_LICENSES)))
            return None, problems
        existing = normalise_license(lic) if lic else ""
        if existing and existing != lic_norm and not force:
            problems.append("existing license %r conflicts with --license %r; use --force to replace it" % (lic, lic_norm))
            return None, problems
        set_field(fields, "license", lic_norm)
    elif lic is not None:
        set_field(fields, "license", normalise_license(lic))
    if title and not TITLE_RE.search(body or ""):
        body = "# %s\n\n%s" % (title, (body or "").lstrip("\n"))
    problems.extend(check_fields(fields, body))
    if problems:
        return None, problems
    return render_card(fields, body), []


def read_input(path):
    if not os.path.exists(path):
        return None, "input file not found: %s" % path
    if not os.path.isfile(path):
        return None, "input path is not a file: %s" % path
    try:
        with open(path, encoding="utf-8-sig") as fh:
            return fh.read(), None
    except (OSError, UnicodeError) as e:
        return None, "could not read input: %s: %s" % (type(e).__name__, e)


def main(argv):
    args = list(argv[1:])
    input_path = None
    output_path = None
    license_value = None
    title = None
    force = False
    check_only = False
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("-o", "--output"):
            if i + 1 >= len(args):
                print("FAIL: %s needs a value" % arg)
                return 2
            output_path = args[i + 1]
            i += 2
        elif arg == "--license" or arg == "--licence":
            if i + 1 >= len(args):
                print("FAIL: %s needs a value" % arg)
                return 2
            license_value = args[i + 1]
            i += 2
        elif arg == "--title":
            if i + 1 >= len(args):
                print("FAIL: --title needs a value")
                return 2
            title = args[i + 1]
            i += 2
        elif arg in ("--force", "--overwrite-license"):
            force = True
            i += 1
        elif arg == "--check-only":
            check_only = True
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
        print("FAIL: usage: python3 dataset_card_licence.py existing_README.md --license mit [-o README.md] [--force] [--check-only]")
        return 2
    text, err = read_input(input_path)
    if err:
        print("FAIL: %s" % err)
        return 1
    if check_only:
        fields, body, problems = parse_card(text)
        problems.extend(check_fields(fields, body))
        if problems:
            for p in problems:
                print("FAIL: %s: %s" % (input_path, p))
            return 1
        print("PASS: %s (license: %s)" % (input_path, get_field(fields, "license")))
        return 0
    card, problems = build_card(text, license_value, force, title)
    if problems:
        for p in problems:
            print("FAIL: %s: %s" % (input_path, p))
        return 1
    if output_path:
        try:
            with open(output_path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(card)
        except OSError as e:
            print("FAIL: could not write output: %s: %s" % (type(e).__name__, e))
            return 1
        print("wrote card to %s" % output_path)
    else:
        sys.stdout.write(card)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
