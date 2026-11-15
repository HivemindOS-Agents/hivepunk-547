#!/usr/bin/env python3
"""Self-test for hf-publish-check-fixtures-cases.

Run from this folder with no arguments and no network. It imports the tool's
own code (generate_cases) and checks:

  1. generate_cases.render() reproduces the shipped cases.csv byte for byte;
  2. the header is exactly case,folder,expected_verdict,expected_detail;
  3. there are exactly four rows, in the fixed order, with the expected
     verdicts (one ready, three not_ready);
  4. README.md names every column and carries the caveat line saying the rows
     are expected verdicts, not a run log, plus the tool link;
  5. stage() copies both uploadable files into a temp folder with the same
     bytes as the shipped ones;
  6. --check agrees on the shipped file and rejects a mutated copy.

Exits 0 only when every check passes.
"""

import csv
import io
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED_COLUMNS = ["case", "folder", "expected_verdict", "expected_detail"]
EXPECTED_CASES = [
    ("good", "fixtures/good", "ready"),
    ("missing_ref", "fixtures/missing_ref", "not_ready"),
    ("bad_front_matter", "fixtures/bad_front_matter", "not_ready"),
    ("missing_readme", "fixtures/missing_readme", "not_ready"),
]
TOOL_LINK = "tools/hf-publish-check"


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
        return __import__("generate_cases")
    except Exception as e:
        raise Fail("could not import generate_cases: %s: %s" % (type(e).__name__, e))


def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return fh.read()


def test_csv_matches(mod):
    produced = mod.render()
    shipped = read("cases.csv")
    check(shipped == produced,
          "render() does not match cases.csv:\n--- shipped ---\n%s\n--- produced ---\n%s"
          % (shipped, produced))
    return "csv: cases.csv reproduced exactly (%d line(s))" % len(produced.splitlines())


def test_rows(mod):
    rows = list(csv.DictReader(io.StringIO(read("cases.csv"))))
    check(list(rows[0].keys()) == EXPECTED_COLUMNS,
          "header is %r, expected %r" % (list(rows[0].keys()), EXPECTED_COLUMNS))
    check(len(rows) == len(EXPECTED_CASES),
          "expected %d rows, got %d" % (len(EXPECTED_CASES), len(rows)))
    for i, (case, folder, verdict) in enumerate(EXPECTED_CASES):
        r = rows[i]
        check(r["case"] == case, "row %d case is %r, expected %r" % (i, r["case"], case))
        check(r["folder"] == folder, "row %d folder is %r, expected %r" % (i, r["folder"], folder))
        check(r["expected_verdict"] == verdict,
              "row %d verdict is %r, expected %r" % (i, r["expected_verdict"], verdict))
        check(r["expected_detail"], "row %d has an empty detail" % i)
    verdicts = [r["expected_verdict"] for r in rows]
    check(verdicts.count("ready") == 1 and verdicts.count("not_ready") == 3,
          "expected 1 ready and 3 not_ready, got %r" % verdicts)
    return "rows: header + %d case(s), 1 ready / 3 not_ready" % len(rows)


def test_card():
    card = read("README.md")
    check(card.startswith("---"), "card does not start with a front-matter block")
    check(card.splitlines()[0].strip() == "---", "card first line is not '---'")
    for col in EXPECTED_COLUMNS:
        check(("`%s`" % col) in card, "card does not name column %r" % col)
    check("not a\nrun log" in card or "not a run log" in card,
          "card lacks the 'expected verdicts, not a run log' caveat")
    check(TOOL_LINK in card, "card does not link %r" % TOOL_LINK)
    check("hivepunk-547" in card, "card does not name the repository owner")
    return "card: columns named, caveat and tool link present"


def test_stage(mod):
    with tempfile.TemporaryDirectory() as tmp:
        written = mod.stage(os.path.join(tmp, "out"))
        check(len(written) == 2, "stage wrote %d file(s), expected 2" % len(written))
        for name in mod.UPLOAD_FILES:
            staged = os.path.join(tmp, "out", name)
            check(os.path.isfile(staged), "stage did not write %s" % name)
            with open(staged, encoding="utf-8") as fh:
                check(fh.read() == read(name), "staged %s differs from the shipped file" % name)
    return "stage: 2 uploadable file(s) copied byte for byte"


def test_check_mode(mod):
    produced = mod.render()
    ok, detail = mod.check_existing(produced)
    check(ok, "--check on the shipped file said: %s" % detail)
    mutated = produced.replace(",not_ready,", ",ready,", 1)
    check(mutated != produced, "mutation helper did not change the text")
    ok2, detail2 = mod.check_existing(mutated)
    check(not ok2, "--check accepted a mutated csv: %s" % detail2)
    check("differs" in detail2, "mutation detail lacks 'differs': %r" % detail2)
    return "check mode: agrees on shipped file, rejects a mutated copy"


def main():
    try:
        mod = import_tool()
        lines = [
            test_csv_matches(mod),
            test_rows(mod),
            test_card(),
            test_stage(mod),
            test_check_mode(mod),
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
