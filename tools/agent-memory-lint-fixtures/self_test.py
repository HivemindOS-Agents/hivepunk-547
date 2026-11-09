#!/usr/bin/env python3
"""Self-test for the agent-memory-lint fixtures.

Run with NO arguments, from this folder. No network, no writes.
Imports the tool's own code (lint.py) and runs it on the bundled fixture
folders, comparing what comes out with what should. Exits 0 only when
every check passes.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def die(msg):
    sys.stderr.write("FAIL: " + msg + "\n")
    sys.exit(1)


def read_text(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def main():
    # Import the linter's function directly
    sys.path.insert(0, HERE)
    from lint import lint_dataset as lint

    # ---- 1. clean fixture (should pass) ----
    clean_path = os.path.join(HERE, "clean")
    if not os.path.isdir(clean_path):
        die("clean/ not found")
    errs = lint(clean_path)
    if errs:
        die("clean/ should have 0 errors, got: " + str(errs))
    print("PASS clean: no errors")

    # ---- 2. bad-rows fixture ----
    bad_rows_path = os.path.join(HERE, "bad-rows")
    if not os.path.isdir(bad_rows_path):
        die("bad-rows/ not found")
    errs = lint(bad_rows_path)
    expected = ["data.csv line 2 has 3 cells (header 4)"]
    if errs != expected:
        die("bad-rows expected " + str(expected) + ", got " + str(errs))
    print("PASS bad-rows: 1 error, line 2 has 3 cells (header 4)")

    # ---- 3. bad-card fixture ----
    bad_card_path = os.path.join(HERE, "bad-card")
    if not os.path.isdir(bad_card_path):
        die("bad-card/ not found")
    errs = lint(bad_card_path)
    expected = ["README missing closing 'What could not be checked' section"]
    if errs != expected:
        die("bad-card expected " + str(expected) + ", got " + str(errs))
    print("PASS bad-card: 1 error, missing closing section")

    print("OK: self-test passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
