#!/usr/bin/env python3
"""Standalone self-test. No args, no network, run alone from this folder.
Checks report/README/ARTIFACTS content. Exit 0 only when all pass.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, "2026-11-22-uniswap-v4-upgrade-watch.md")
README = os.path.join(HERE, "README.md")
ART = os.path.join(HERE, "ARTIFACTS.md")
ASK = "https://github.com/for-toolathlon/uniswap-v4-watch/issues/1"
SOURCES = [
 "https://www.datawallet.com/crypto/uniswap-v4-explained",
 "https://blog.uniswap.org/uniswap-v4",
 "https://www.spark.money/research/ethereum-uniswap-v4-hooks-defi-payments",
 "https://dev.to/frb_research/uniswap-v4-hooks-mev-2026-searcher-opportunities-and-risks-1ff7",
 "https://ryder.id/blogs/post/uniswap-v4-hooks-in-2026-what-they-mean-for-signers",
 "https://hacken.io/discover/auditing-uniswap-v4-hooks/",
]
def read(p):
    if not os.path.exists(p):
        sys.stderr.write("FAIL: missing %s\n" % os.path.basename(p)); sys.exit(1)
    return open(p, encoding="utf-8").read()
def main():
    report, readme, art = read(REPORT), read(README), read(ART)
    checks = []
    def need(cond, msg):
        if not cond:
            sys.stderr.write("FAIL: %s\n" % msg); sys.exit(1)
    need("2026-11-22" in report and "Uniswap v4" in report, "report date/title")
    need(ASK in report and ASK in readme, "ask link in report and README")
    for label in ("FACT", "DERIVED", "UNKNOWN"):
        need(label in report, "report missing label %s" % label)
    need(report.count("| FACT |") == 9, "FACT table rows %d != 9" % report.count("| FACT |"))
    need(report.count("| DERIVED |") == 1, "DERIVED table rows != 1")
    need(report.count("| UNKNOWN |") == 2, "UNKNOWN table rows != 2")
    for url in SOURCES:
        need(url in report, "report missing source %s" % url)
    need("PoolManager" in report and "31 January 2025" in report and "$484 billion" in report, "key report claims")
    need("Could not confirm" in report, "report could-not-confirm")
    checks.append("report has date, ask link, FACT 9/DERIVED 1/UNKNOWN 2 and all six sources")
    need("Caveats first" in readme and "UNTESTED" in readme and "FACT" in readme and "UNKNOWN" in readme, "README caveats/untested")
    need("python3 self_test.py" in readme, "README command")
    checks.append("README has caveats first, untested marks and command")
    need("2026-11-22-uniswap-v4-upgrade-watch.md" in art and "python3 self_test.py" in art and "NOT confirmed" in art and "Left for owner" in art, "ARTIFACTS entry")
    checks.append("ARTIFACTS.md records artifacts, command, NOT confirmed and left-for-owner")
    for line in checks: print(line)
    print("self-test: all checks passed")
    return 0
if __name__ == "__main__":
    sys.exit(main())
