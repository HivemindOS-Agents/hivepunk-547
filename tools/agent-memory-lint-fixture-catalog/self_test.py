#!/usr/bin/env python3
"""Self-test for agent-memory-lint-fixture-catalog.

Run from this folder with no arguments and no network. It imports the tool's
own code (generate_catalog) and checks:

  1. importing generate_catalog works (the earlier failure was the missing
     `from textwrap import dedent` import in generate_catalog.py);
  2. make_catalog(sample=True) reproduces the shipped catalog.csv byte for byte;
  3. catalog.csv has the expected header and exactly one row for each of the
     three fixture paths, in order;
  4. `--check` mode agrees on the shipped file and disagrees on a mutated copy.

Exits 0 only when every check passes.
"""

import io
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED_PATHS = ["fixtures/clean/", "fixtures/bad-rows/", "fixtures/bad-card/"]


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
        return __import__("generate_catalog")
    except Exception as e:
        raise Fail("could not import generate_catalog: %s: %s" % (type(e).__name__, e))


def test_sample(mod):
    produced = mod.make_catalog(sample=True)
    with open(os.path.join(HERE, "catalog.csv"), encoding="utf-8") as fh:
        shipped = fh.read()
    check(shipped == produced,
          "sample output does not match catalog.csv:\n--- shipped ---\n%s\n--- produced ---\n%s"
          % (shipped, produced))
    return "sample: catalog.csv reproduced exactly (%d line(s))" % len(produced.splitlines())


def test_shape(mod):
    produced = mod.make_catalog(sample=True)
    lines = produced.splitlines()
    check(lines[0] == ",".join(mod.COLUMNS),
          "header is %r, expected %r" % (lines[0], ",".join(mod.COLUMNS)))
    check(len(lines) == 1 + len(EXPECTED_PATHS),
          "expected %d lines, got %d" % (1 + len(EXPECTED_PATHS), len(lines)))
    for i, path in enumerate(EXPECTED_PATHS, 1):
        check(lines[i].startswith(path + ","),
              "line %d should start with %r, got %r" % (i, path + ",", lines[i]))
    check("clean" in lines[1] and ",0," in lines[1],
          "clean row should carry expected exit code 0: %r" % lines[1])
    check(",1," in lines[2] and ",1," in lines[3],
          "bad rows/card should carry expected exit code 1: %r %r" % (lines[2], lines[3]))
    return "shape: header + %d fixture row(s) in fixed order" % len(EXPECTED_PATHS)


def test_check_mode(mod):
    produced = mod.make_catalog(sample=True)
    ok, detail = mod.check_existing(produced)
    check(ok, "--check on the shipped file said: %s" % detail)
    mutated = produced.replace(",1,", ",9,", 1)
    check(mutated != produced, "mutation helper did not change the text")
    ok2, detail2 = mod.check_existing(mutated)
    check(not ok2, "--check accepted a mutated catalog: %s" % detail2)
    check("differs" in detail2, "mutation detail lacks 'differs': %r" % detail2)
    return "check mode: agrees on shipped file, rejects a mutated copy"


def main():
    try:
        mod = import_tool()
        lines = [
            test_sample(mod),
            test_shape(mod),
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
