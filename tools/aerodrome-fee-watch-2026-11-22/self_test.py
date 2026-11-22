#!/usr/bin/env python3
"""Standalone self-test. No args, no network, run alone from this folder."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = "2026-11-22-aerodrome-fee-watch.md"
SOURCES = [
 "https://thedefireport.io/research/the-watch-list-aerodrome-aero",
 "https://github.com/fullstack-development/blockchain-wiki-en/blob/main/protocols/aerodrome/README.md",
 "https://www.onebullex.com/explore/technology-behind-aero-unique",
 "https://www.coincu.com/aerodrome-review-2026-how-the-veaero-flywheel-works-on-base/",
 "https://api.github.com/repos/fullstack-development/blockchain-wiki-en/commits?per_page=50&since=2026-10-23T15:13:21.772Z",
]
RESEARCH = "https://github.com/HivemindOS-Agents/hivepunk-547/blob/main/research/2026-11-22-aerodrome-finance.md"
def read(name):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        sys.stderr.write("FAIL: missing %s\n" % name); sys.exit(1)
    return open(p, encoding="utf-8").read()
def main():
    report, readme, art = read(REPORT), read("README.md"), read("ARTIFACTS.md")
    def need(cond, msg):
        if not cond:
            sys.stderr.write("FAIL: %s\n" % msg); sys.exit(1)
    need("2026-11-22" in report and "Aerodrome" in report and "fee/liquidity" in report, "report date/title")
    need(RESEARCH in report, "research-note link in report")
    for label in ("FACT", "DERIVED", "UNKNOWN"):
        need(label in report, "report label %s" % label)
    need(report.count("| FACT |") == 5, "FACT rows %d != 5" % report.count("| FACT |"))
    need(report.count("| DERIVED |") == 2, "DERIVED rows %d != 2" % report.count("| DERIVED |"))
    need(report.count("| UNKNOWN |") == 3, "UNKNOWN rows %d != 3" % report.count("| UNKNOWN |"))
    for url in SOURCES:
        need(url in report, "report source %s" % url)
    need("August 2023" in report and "concentrated-liquidity" in report and "Velodrome" in report and "veAERO" in report, "key report claims")
    need("Caveats first" in report and "Could not confirm" in report, "report caveats")
    print("report has date, FACT 5/DERIVED 2/UNKNOWN 3 and all five sources")
    need("Caveats first" in readme and "UNTESTED" in readme and "python3 self_test.py" in readme, "README caveats/untested/command")
    need(RESEARCH in readme or "research/2026-11-22-aerodrome-finance.md" in readme, "README research link")
    need("agent-memory-lint-fixtures" in readme, "README do-not-touch note")
    print("README has caveats first, untested marks, command, do-not-touch note")
    need("2026-11-22-aerodrome-fee-watch.md" in art and "python3 self_test.py" in art, "ARTIFACTS list/command")
    need("NOT confirmed" in art and "Commit note" in art and "Left for owner" in art, "ARTIFACTS not-confirmed/commit/owner")
    print("ARTIFACTS.md records artifacts, command, NOT confirmed, commit note, left-for-owner")
    print("self-test: all checks passed")
    return 0
if __name__ == "__main__":
    sys.exit(main())
