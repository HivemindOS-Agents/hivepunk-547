#!/usr/bin/env python3
"""Standalone self-test. No args, no network, run alone from this folder."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
def read(name):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        sys.stderr.write("FAIL: missing %s\n" % name); sys.exit(1)
    return open(p, encoding="utf-8").read()
def main():
    readme, art = read("README.md"), read("ARTIFACTS.md")
    def need(c, m):
        if not c:
            sys.stderr.write("FAIL: %s\n" % m); sys.exit(1)
    need("Caveats first" in readme and "UNTESTED" in readme and "python3 self_test.py" in readme, "README caveats/untested/command")
    need("fixprotocol-modifyliquidities-nonreentrant" in readme, "README folder name")
    print("README has caveats first, untested marks and command")
    need("README.md" in art and "self_test.py" in art and "ARTIFACTS.md" in art, "ARTIFACTS list")
    need("python3 self_test.py" in art, "ARTIFACTS exact command")
    need("tools/fixprotocol-modifyliquidities-nonreentrant/" in art, "ARTIFACTS folder path")
    need("Raw stdout, stderr and exit code" in art, "ARTIFACTS raw-output slot")
    need("NOT confirmed" in art and "Commit note" in art and "Left for owner" in art, "ARTIFACTS not-confirmed/commit-note/owner")
    print("ARTIFACTS.md records artifacts, exact command, raw-output slot, NOT confirmed, commit note, left-for-owner")
    print("self-test: all checks passed")
    return 0
if __name__ == "__main__":
    sys.exit(main())
