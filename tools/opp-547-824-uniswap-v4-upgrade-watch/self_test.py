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
    tracker, readme, art = read("tracker.md"), read("README.md"), read("ARTIFACTS.md")
    def need(c, m):
        if not c:
            sys.stderr.write("FAIL: %s\n" % m); sys.exit(1)
    ASK2 = "https://github.com/for-toolathlon/uniswap-v4-watch-2/issues/1"
    ASK1 = "https://github.com/for-toolathlon/uniswap-v4-watch/issues/1"
    need(ASK2 in tracker and ASK2 in readme and ASK2 in art, "watch-2 ask link")
    need(ASK1 in tracker and ASK1 in readme, "prior ask link")
    for label in ("FACT", "DERIVED", "UNKNOWN"):
        need(label in tracker, "tracker label %s" % label)
    need("Caveats first" in tracker and "Could not confirm" in tracker, "tracker caveats")
    need("Child issues confirmed: 0" in tracker, "tracker child count honesty")
    need(tracker.count("UNKNOWN - not fetched") >= 1 and "none confirmed" in tracker, "child UNKNOWN placeholders")
    need("not fetched" in readme and "not fetched" in tracker, "not-fetched honesty")
    need(tracker.count("| FACT |") == 3, "context FACT rows %d" % tracker.count("| FACT |"))
    need(tracker.count("| DERIVED |") == 1, "context DERIVED rows")
    need(tracker.count("| UNKNOWN |") == 2, "context UNKNOWN rows")
    for url in ("https://blog.uniswap.org/uniswap-v4", "https://www.datawallet.com/crypto/uniswap-v4-explained", "https://hacken.io/discover/auditing-uniswap-v4-hooks/"):
        need(url in tracker, "tracker source %s" % url)
    print("tracker has both asks, FACT 3/DERIVED 1/UNKNOWN 2 context, UNKNOWN child honesty, sources")
    need("Caveats first" in readme and "UNTESTED" in readme and "python3 self_test.py" in readme, "README caveats/untested/command")
    need("agent-memory-lint-fixtures" in readme, "README do-not-touch note")
    print("README has caveats first, untested marks, command, do-not-touch note")
    need("tracker.md" in art and "README.md" in art and "self_test.py" in art, "ARTIFACTS list")
    need("python3 self_test.py" in art and "NOT confirmed" in art and "Commit note" in art and "Left for owner" in art, "ARTIFACTS command/not-confirmed/commit-note/owner")
    print("ARTIFACTS.md records artifacts, command, NOT confirmed, commit note, left-for-owner")
    print("self-test: all checks passed")
    return 0
if __name__ == "__main__":
    sys.exit(main())
