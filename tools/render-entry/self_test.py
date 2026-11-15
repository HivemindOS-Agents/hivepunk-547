#!/usr/bin/env python3
"""Self-test for hf-publish-check-artifacts-entry.

Run from this folder with no arguments and no network. It imports the tool's
own code (render_entry) and checks the pass-claim gate:

  1. build_row carries the tool folder, both file URLs and the self-test path;
  2. a synthetic transcript whose raw output shows exit code 0 renders
     'status: passed';
  3. a synthetic transcript with exit code 1 renders 'status: unconfirmed'
     and never 'passed';
  4. the no-transcript case renders 'status: unconfirmed' and names the
     missing transcript;
  5. the recorded run URL is present in the row.

Exits 0 only when every check passes.
"""

import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


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
        return __import__("render_entry")
    except Exception as e:
        raise Fail("could not import render_entry: %s: %s" % (type(e).__name__, e))


def write_transcript(tmp, text):
    path = os.path.join(tmp, "SELFTEST_OUTPUT.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def test_row_has_required_parts(mod):
    entry = mod.load_entry()
    row = mod.build_row(entry, transcript_path=os.path.join(HERE, "does-not-exist.md"))
    check(entry["tool_folder"] in row, "row lacks the tool folder")
    for url in entry["files"]:
        check(url in row, "row lacks file url %s" % url)
    check(entry["self_test"] in row, "row lacks the self-test path")
    check("cases.csv" in row and "README.md" in row, "row does not name both files")
    return "row: tool folder, both file urls and self-test path present"


def test_pass_only_on_exit_zero(mod):
    entry = mod.load_entry()
    with tempfile.TemporaryDirectory() as tmp:
        p0 = write_transcript(tmp, "a check line\nexit code: 0\n")
        row0 = mod.build_row(entry, transcript_path=p0)
        check("status: passed" in row0,
              "exit-0 transcript did not render status: passed:\n%s" % row0)
        p1 = write_transcript(tmp, "a check line\nexit code: 1\n")
        row1 = mod.build_row(entry, transcript_path=p1)
        check("status: unconfirmed" in row1,
              "exit-1 transcript did not stay unconfirmed:\n%s" % row1)
        check("passed" not in row1.replace("unconfirmed", ""),
              "exit-1 transcript claimed a pass:\n%s" % row1)
    return "gate: passed only on a raw exit code 0, unconfirmed on exit 1"


def test_no_transcript(mod):
    entry = mod.load_entry()
    row = mod.build_row(entry, transcript_path=os.path.join(HERE, "nope.md"))
    check("status: unconfirmed" in row,
          "no-transcript case did not stay unconfirmed:\n%s" % row)
    check("SELFTEST_OUTPUT.md" in row,
          "no-transcript detail does not name the missing transcript:\n%s" % row)
    return "no transcript: status unconfirmed, missing name given"


def test_bare_last_line(mod):
    entry = mod.load_entry()
    with tempfile.TemporaryDirectory() as tmp:
        p = write_transcript(tmp, "self-test: all checks passed\n0\n")
        with open(p, encoding="utf-8") as fh:
            text = fh.read()
        code, how = mod.read_exit_code(text)
        check(code == 0, "bare final 0 not read as exit code: %r (%s)" % (code, how))
    return "exit code: read from a bare final integer line too"


def test_records_run_url(mod):
    entry = mod.load_entry()
    row = mod.build_row(entry, transcript_path=os.path.join(HERE, "nope.md"))
    run = entry.get("recorded_run", {}).get("run", "")
    check(run and run in row, "row lacks the recorded run url")
    return "row: recorded run url present"


def main():
    try:
        mod = import_tool()
        lines = [
            test_row_has_required_parts(mod),
            test_pass_only_on_exit_zero(mod),
            test_no_transcript(mod),
            test_bare_last_line(mod),
            test_records_run_url(mod),
        ]
    except Fail as e:
        sys.stderr.write("FAIL: %s\n" % e)
        return 1
    except Exception as e:
        sys.stderr.write("FAIL: unexpected %s: %s\n" % (type(e).__name__, e))
        return 1
    for line in lines:
        print(line)
    print("self-test: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
