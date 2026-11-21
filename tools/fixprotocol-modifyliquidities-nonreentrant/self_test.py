#!/usr/bin/env python3
"""Self-test: check patch + docs content. No args, no network."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PATCH = os.path.join(HERE, "modifyLiquidities-nonReentrant.patch")
README = os.path.join(HERE, "README.md")
GOAL = os.path.join(HERE, "GOAL.md")
ISSUE = "https://github.com/RigoBlock/v3-contracts/issues/1020"
def read(p):
    if not os.path.exists(p):
        sys.stderr.write("FAIL: missing %s\n" % os.path.basename(p)); sys.exit(1)
    return open(p, encoding="utf-8").read()
def main():
    patch, readme, goal = read(PATCH), read(README), read(GOAL)
    checks = []
    def need(cond, msg):
        if not cond:
            sys.stderr.write("FAIL: %s\n" % msg); sys.exit(1)
    need("modifyLiquidities" in patch, "patch does not name modifyLiquidities")
    need("nonReentrant" in patch, "patch does not add nonReentrant")
    need("external nonReentrant" in patch, "patch must add modifier to external declaration")
    need(patch.count("modifyLiquidities") >= 1 and "-    function modifyLiquidities" in patch and "+    function modifyLiquidities(...) external nonReentrant" in patch, "patch must be a one-line -/+ replacement")
    need(ISSUE in patch, "patch missing issue link")
    need("UNTESTED" in patch, "patch must mark itself untested")
    checks.append("patch adds nonReentrant to modifyLiquidities with issue link and untested note")
    need("UNTESTED DEPLOYMENT" in readme, "README must state untested deployment")
    need("NOT been deployed" in readme and "NOT been compiled" in readme, "README untested scope")
    need("ReentrancyGuard" in readme and "import" in readme.lower(), "README import note")
    need("last" in readme and "onlyOwner" in readme, "README ordering note")
    checks.append("README states untested deployment and import/ordering notes")
    need(ISSUE in goal and "ARTIFACTS" in goal and "modifyLiquidities-nonReentrant.patch" in goal, "GOAL artifacts record")
    need("NOT confirmed" in goal, "GOAL must state what was not confirmed")
    checks.append("GOAL records issue, artifacts and unconfirmed items")
    for line in checks: print(line)
    print("self-test: all checks passed")
    return 0
if __name__ == "__main__":
    sys.exit(main())
