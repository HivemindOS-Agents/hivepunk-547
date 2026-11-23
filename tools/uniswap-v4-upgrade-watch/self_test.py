#!/usr/bin/env python3
"""Standalone self-test. No args, no network, run alone from this folder."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
def read(name):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        sys.stderr.write("FAIL: missing %s\n" % name); sys.exit(1)
    return open(p, encoding="utf-8").read()
def main():
    seed_text, readme, art = read("seed_row.json"), read("README.md"), read("ARTIFACTS.md")
    def need(c, m):
        if not c:
            sys.stderr.write("FAIL: %s\n" % m); sys.exit(1)
    try:
        seed = json.loads(seed_text)
    except Exception as e:
        sys.stderr.write("FAIL: seed_row.json invalid JSON: %s\n" % e); sys.exit(1)
    need(seed.get("repository") == "Uniswap/v4-core", "seed repository")
    need(seed.get("latest_release_tag") == "UNKNOWN", "latest_release_tag UNKNOWN")
    need(seed.get("latest_release_date") == "UNKNOWN", "latest_release_date UNKNOWN")
    need(seed.get("verified_latest_release_tag") == "UNKNOWN", "verified tag UNKNOWN")
    need(seed.get("verified_latest_release_date") == "UNKNOWN", "verified date UNKNOWN")
    need("UNKNOWN" in str(seed.get("verification_status", "")), "verification_status UNKNOWN")
    need(seed.get("releases_url") == "https://github.com/Uniswap/v4-core/releases", "releases_url")
    need(seed.get("repository_url") == "https://github.com/Uniswap/v4-core", "repository_url")
    claims = seed.get("unverified_claims", [])
    need(len(claims) == 1, "exactly one unverified claim")
    claim = claims[0]
    need(claim.get("release_tag") == "v4.0.0" and claim.get("release_date") == "2025-01-23", "unverified v4.0.0/2025-01-23")
    need("unverified" in str(claim.get("status", "")), "claim status unverified")
    need(claim.get("release_tag") != seed.get("verified_latest_release_tag"), "claim separate from verified")
    sources = seed.get("sources", [])
    need("https://github.com/Uniswap/v4-core/releases" in sources, "source releases URL")
    need("https://github.com/Uniswap/v4-core" in sources, "source repo URL")
    print("seed_row.json: verified UNKNOWN, unverified v4.0.0/2025-01-23 separate, sources present")
    need("Caveats first" in readme and "UNTESTED" in readme and "python3 self_test.py" in readme, "README caveats/untested/command")
    need("UNKNOWN" in readme and "https://github.com/Uniswap/v4-core/releases" in readme, "README UNKNOWN and releases URL")
    print("README has caveats first, untested marks, command, UNKNOWN honesty")
    need("seed_row.json" in art and "README.md" in art and "self_test.py" in art and "ARTIFACTS.md" in art, "ARTIFACTS list")
    need("python3 self_test.py" in art, "ARTIFACTS exact command")
    need("tools/uniswap-v4-upgrade-watch/" in art, "ARTIFACTS folder path")
    need("Raw stdout, stderr and exit code" in art, "ARTIFACTS verification output slot")
    need("NOT confirmed" in art and "Commit note" in art and "Left for owner" in art, "ARTIFACTS not-confirmed/commit-note/owner")
    print("ARTIFACTS.md records artifacts, command, verification slot, NOT confirmed, commit note, left-for-owner")
    print("self-test: all checks passed")
    return 0
if __name__ == "__main__":
    sys.exit(main())
