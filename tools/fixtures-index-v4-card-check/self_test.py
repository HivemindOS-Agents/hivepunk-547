#!/usr/bin/env python3
"""Self-test for fixtures-index-v4-card-check.

Run from this folder with no arguments and no network. Imports
card_check, checks the included README.md + data.csv pass, then checks
synthetic cards in a temp directory: no frontmatter, missing license,
empty language, empty tags, wrong dataset name, file list missing a
name, file list with an extra name, no Files section, and a missing
data.csv. Also checks CLI exit 0/1. Exits 0 only if all checks pass.
"""

import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "fixtures-index-v4"
FILES = ["inventory.py", "self_test.py", "README.md", "INVENTORY.md"]
CSV_TEXT = "file_name,source_url,description\n" + "".join(
    "%s,https://example.com/tools/fixtures-index-v4/%s,desc for %s\n" % (n, n, n)
    for n in FILES)


class Fail(Exception):
    pass


def check(cond, msg):
    if not cond:
        raise Fail(msg)


def import_tool():
    sys.dont_write_bytecode = True
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    try:
        return __import__("card_check")
    except Exception as e:
        raise Fail("could not import card_check: %s: %s" % (type(e).__name__, e))


def make_card(files=None, name=NAME, license="mit", language="en",
              tags="- fixtures\n- inventory", frontmatter=True):
    files = FILES if files is None else files
    parts = []
    if frontmatter:
        parts.append("---\nlicense: %s\nlanguage: %s\ntags:\n%s\n---\n" % (license, language, tags))
    parts.append("# %s\n\n## Files\n\n" % name)
    parts.extend("- %s\n" % f for f in files)
    parts.append("\n## Untested\n\nNone.\n")
    return "".join(parts)


def write(folder, name, text):
    path = os.path.join(folder, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def main():
    try:
        mod = import_tool()
        checks = []

        ok, problems, listed = mod.verify(
            os.path.join(HERE, "README.md"), os.path.join(HERE, "data.csv"), NAME)
        check(ok, "included card failed: %r" % (problems,))
        check(listed == FILES, "included Files list is %r" % (listed,))
        checks.append("included README.md + data.csv pass: %s" % ", ".join(FILES))

        with tempfile.TemporaryDirectory() as tmp:
            csv_path = write(tmp, "data.csv", CSV_TEXT)
            readme_path = write(tmp, "README.md", make_card())
            ok, problems, _ = mod.verify(readme_path, csv_path, NAME)
            check(ok, "synthetic good card failed: %r" % (problems,))
            checks.append("synthetic good card passes")

            inline = write(tmp, "inline.md", make_card(tags="[fixtures, inventory]"))
            ok, problems, _ = mod.verify(inline, csv_path, NAME)
            check(ok, "inline tags card failed: %r" % (problems,))
            checks.append("inline [..] tags form passes")

            cases = [
                ("no frontmatter", make_card(frontmatter=False), "frontmatter"),
                ("missing license", make_card(license=""), "license is empty"),
                ("empty language", make_card(language=""), "language is empty"),
                ("empty tags", make_card(tags="[]"), "tags is empty"),
                ("wrong dataset name", make_card(name="other-dataset"), "dataset name"),
                ("file list missing", make_card(files=FILES[:3]), "missing from card"),
                ("file list extra", make_card(files=FILES + ["extra.py"]), "extra names"),
                ("file list duplicate", make_card(files=FILES + [FILES[0]]), "duplicate"),
            ]
            for label, text, needle in cases:
                path = write(tmp, label.replace(" ", "_") + ".md", text)
                ok, problems, _ = mod.verify(path, csv_path, NAME)
                check(not ok, "%s unexpectedly passed" % label)
                check(any(needle in p for p in problems),
                      "%s problems %r do not mention %r" % (label, problems, needle))
                checks.append("%s fails and mentions %r" % (label, needle))

            no_section = "---\nlicense: mit\nlanguage: en\ntags:\n- fixtures\n---\n\n# %s\n\nNo list here.\n" % NAME
            path = write(tmp, "no_section.md", no_section)
            ok, problems, _ = mod.verify(path, csv_path, NAME)
            check(not ok and any("Files" in p for p in problems),
                  "no Files section: %r" % (problems,))
            checks.append("missing Files section fails and mentions 'Files'")

            ok, problems, _ = mod.verify(readme_path, os.path.join(tmp, "missing.csv"), NAME)
            check(not ok and any("not found" in p for p in problems),
                  "missing csv: %r" % (problems,))
            checks.append("missing data.csv fails with 'not found'")

            code = mod.main(["card_check.py", readme_path, csv_path, NAME])
            check(code == 0, "CLI good returned %r" % code)
            bad = write(tmp, "bad.md", make_card(name="wrong"))
            code = mod.main(["card_check.py", bad, csv_path, NAME])
            check(code == 1, "CLI bad returned %r" % code)
            checks.append("CLI exits 0 for good card and 1 for bad card")
    except Fail as e:
        sys.stderr.write("FAIL: %s\n" % e)
        return 1
    except Exception as e:
        sys.stderr.write("FAIL: unexpected %s: %s\n" % (type(e).__name__, e))
        return 1
    for line in checks:
        print(line)
    print("self-test: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
