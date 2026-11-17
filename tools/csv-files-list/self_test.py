#!/usr/bin/env python3
"""Self-test for csv-files-list.

Run from this folder with no arguments and no network. Imports
csv_files, checks the included data.csv, then checks local synthetic
CSVs in a temp directory: normal rows, quoted names (including a quoted
name containing a comma), and blank rows, plus failure cases (missing
file_name column, missing file, duplicate, empty file_name in a
non-blank row) and CLI exit codes. Exits 0 only if all checks pass.
"""

import contextlib
import io
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
EXPECTED = ["inventory.py", "self_test.py", "README.md", "INVENTORY.md"]


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
        return __import__("csv_files")
    except Exception as e:
        raise Fail("could not import csv_files: %s: %s" % (type(e).__name__, e))


def write(folder, name, text):
    path = os.path.join(folder, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def parse_card_bullets(markdown):
    # Same bullet shape card_check.py accepts: '- name' with no spaces.
    names = []
    for line in markdown.splitlines():
        m = re.match(r"^\s*[-*]\s+`?([^`\s]+)`?\s*$", line)
        if m:
            names.append(m.group(1))
    return names


def main():
    try:
        mod = import_tool()
        checks = []

        ok, problems, names = mod.verify(os.path.join(HERE, "data.csv"))
        check(ok, "included data.csv failed: %r" % (problems,))
        check(names == EXPECTED, "included data.csv names are %r" % (names,))
        md = mod.render_markdown(names)
        check(md == "## Files\n\n- inventory.py\n- self_test.py\n"
                    "- README.md\n- INVENTORY.md\n",
              "included Markdown is %r" % (md,))
        check(parse_card_bullets(md) == EXPECTED,
              "card-check bullet parse of included Markdown differs")
        checks.append("included data.csv renders card-check Files list: %s"
                      % ", ".join(EXPECTED))

        with tempfile.TemporaryDirectory() as tmp:
            normal = write(tmp, "normal.csv",
                           "file_name,description\nalpha.py,First\nbeta.py,Second\n")
            ok, problems, names = mod.verify(normal)
            check(ok and names == ["alpha.py", "beta.py"],
                  "normal CSV: %r %r" % (problems, names))
            check(mod.render_markdown(names)
                  == "## Files\n\n- alpha.py\n- beta.py\n",
                  "normal Markdown mismatch")
            checks.append("normal CSV passes and renders in order")

            quoted = write(tmp, "quoted.csv",
                           'file_name,description\n'
                           '"quoted.py",Has quotes\n'
                           '"data,set.csv",Comma inside quotes\n'
                           'plain.py,No quotes\n')
            ok, problems, names = mod.verify(quoted)
            check(ok, "quoted CSV failed: %r" % (problems,))
            check(names == ["quoted.py", "data,set.csv", "plain.py"],
                  "quoted names are %r" % (names,))
            check(parse_card_bullets(mod.render_markdown(names)) == names,
                  "quoted Markdown does not parse back in card-check format")
            checks.append("quoted names (incl. comma) pass and parse back")

            blank = write(tmp, "blank.csv",
                          "file_name,description\n"
                          "one.py,First\n"
                          "\n"
                          "two.py,Second\n"
                          ",\n"
                          "three.py,Third\n")
            ok, problems, names = mod.verify(blank)
            check(ok, "blank-row CSV failed: %r" % (problems,))
            check(names == ["one.py", "two.py", "three.py"],
                  "blank-row names are %r" % (names,))
            checks.append("blank rows are skipped")

            cases = [
                ("missing column", "name,description\nx.py,Desc\n", "no file_name column"),
                ("duplicate", "file_name\nx.py\nx.py\n", "duplicate"),
                ("empty name", "file_name,description\nx.py,Desc\n,No name\n", "empty file_name"),
                ("no values", "file_name,description\n\n", "no file_name values"),
            ]
            for label, text, needle in cases:
                path = write(tmp, label.replace(" ", "_") + ".csv", text)
                ok, problems, _ = mod.verify(path)
                check(not ok, "%s unexpectedly passed" % label)
                check(any(needle in p for p in problems),
                      "%s problems %r do not mention %r" % (label, problems, needle))
                checks.append("%s fails and mentions %r" % (label, needle))

            ok, problems, _ = mod.verify(os.path.join(tmp, "missing.csv"))
            check(not ok and any("not found" in p for p in problems),
                  "missing file: %r" % (problems,))
            checks.append("missing file fails with 'not found'")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["csv_files.py", normal])
            check(code == 0, "CLI good returned %r" % code)
            check(buf.getvalue() == "## Files\n\n- alpha.py\n- beta.py\n",
                  "CLI good output is %r" % (buf.getvalue(),))
            bad = write(tmp, "cli_bad.csv", "name\nx.py\n")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["csv_files.py", bad])
            check(code == 1, "CLI bad returned %r" % code)
            check("FAIL:" in buf.getvalue(), "CLI bad output is %r" % (buf.getvalue(),))
            checks.append("CLI exits 0 with Markdown for good CSV and 1 with FAIL for bad CSV")
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
