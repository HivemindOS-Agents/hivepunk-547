#!/usr/bin/env python3
"""Self-test for fixtures-index-v4-files-inventory.

Run from this folder with no arguments and no network. Imports
build_dataset, checks the four records, the rendered CSV, the
on-disk data.csv and README card, and a fresh build in a temp folder.
Exits 0 only when every check passes.
"""

import csv
import io
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
EXPECTED_NAMES = ["inventory.py", "self_test.py", "README.md", "INVENTORY.md"]


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
        return __import__("build_dataset")
    except Exception as e:
        raise Fail("could not import build_dataset: %s: %s" % (type(e).__name__, e))


def main():
    try:
        mod = import_tool()
        checks = []

        names = [r["file_name"] for r in mod.RECORDS]
        check(names == EXPECTED_NAMES, "record names are %r" % (names,))
        checks.append("four records in order: " + ", ".join(names))

        for rec in mod.RECORDS:
            check(set(rec) == set(mod.COLUMNS), "%s columns %r" % (rec["file_name"], sorted(rec)))
            check(rec["source_url"] == mod.BLOB_BASE + rec["file_name"],
                  "%s source_url %r" % (rec["file_name"], rec["source_url"]))
            check(rec["description"].strip() and len(rec["description"]) > 20,
                  "%s description too short" % rec["file_name"])
            check("," not in rec["description"], "%s description has a comma" % rec["file_name"])
        checks.append("every record has exact columns, blob source_url and a plain description")

        text = mod.render_csv()
        rows = list(csv.DictReader(io.StringIO(text)))
        check([r["file_name"] for r in rows] == EXPECTED_NAMES, "rendered CSV names wrong")
        check(text.splitlines()[0] == "file_name,source_url,description", "CSV header wrong")
        checks.append("rendered CSV has header plus 4 rows with the right names")

        with open(os.path.join(HERE, "data.csv"), encoding="utf-8") as fh:
            on_disk = fh.read()
        check(on_disk == text, "data.csv on disk differs from render_csv() output")
        checks.append("data.csv on disk matches render_csv() exactly")

        with open(os.path.join(HERE, "README.md"), encoding="utf-8") as fh:
            card = fh.read()
        check(card == mod.README_TEXT, "README.md on disk differs from README_TEXT")
        for needle in (mod.SOURCE_FOLDER, "SELFTEST_OUTPUT.md",
                       "was not written in the build step", "file_name",
                       "source_url", "description", "inventory.py", "INVENTORY.md"):
            check(needle in card, "README card missing %r" % needle)
        checks.append("README card names source folder and the SELFTEST_OUTPUT.md build-step fact")

        with tempfile.TemporaryDirectory() as tmp:
            csv_path, readme_path = mod.write_files(tmp)
            with open(csv_path, encoding="utf-8") as fh:
                check(fh.read() == text, "fresh data.csv differs")
            with open(readme_path, encoding="utf-8") as fh:
                check(fh.read() == card, "fresh README.md differs")
        checks.append("fresh build in a temp folder reproduces data.csv and README.md")
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
