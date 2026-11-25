#!/usr/bin/env python3
"""Standalone self-test. No args, no network, run alone from this folder.

Imports and runs this folder's own watch.py on data/seed_row.json sample
data and compares its output against the expected verified values.
"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import watch
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
    need(seed.get("latest_release_tag") == "v4.0.0", "latest_release_tag v4.0.0")
    need(seed.get("latest_release_date") == "2025-01-23T19:00:03Z", "latest_release_date")
    need(seed.get("verified_latest_release_tag") == "v4.0.0", "verified tag v4.0.0")
    need(seed.get("verified_latest_release_date") == "2025-01-23T19:00:03Z", "verified date")
    need("verified_from_github_api" in str(seed.get("verification_status", "")), "verification_status")
    need(seed.get("source_url") == "https://api.github.com/repos/Uniswap/v4-core/releases/latest", "source_url API")
    need(seed.get("release_id") == 196495150, "release_id 196495150")
    need(seed.get("prerelease") == False, "prerelease false")
    need(seed.get("draft") == False, "draft false")
    need(seed.get("releases_url") == "https://github.com/Uniswap/v4-core/releases", "releases_url")
    need(seed.get("repository_url") == "https://github.com/Uniswap/v4-core", "repository_url")
    sources = seed.get("sources", [])
    need("https://api.github.com/repos/Uniswap/v4-core/releases/latest" in sources, "source API URL")
    need("https://github.com/Uniswap/v4-core/releases" in sources, "source releases URL")
    need("https://github.com/Uniswap/v4-core" in sources, "source repo URL")
    print("seed_row.json: verified v4.0.0/2025-01-23T19:00:03Z, release_id 196495150, prerelease/draft false, sources present")
    sample_path = os.path.join(HERE, "data", "seed_row.json")
    need(os.path.exists(sample_path), "data/seed_row.json sample present")
    sample = json.loads(read(os.path.join("data", "seed_row.json")))
    need(sample == seed, "data/seed_row.json matches root seed_row.json")
    summary = watch.load_seed(sample_path)
    expected = {"repository": "Uniswap/v4-core", "tag": "v4.0.0", "date": "2025-01-23T19:00:03Z", "release_id": 196495150, "prerelease": False, "draft": False, "source_url": "https://api.github.com/repos/Uniswap/v4-core/releases/latest"}
    need(summary == expected, "watch.load_seed(data/seed_row.json) output: %r" % (summary,))
    print("watch.load_seed(data/seed_row.json): %s/%s release_id 196495150" % (summary["tag"], summary["date"]))
    proc = subprocess.run([sys.executable, os.path.join(HERE, "watch.py"), sample_path], capture_output=True, text=True, timeout=30)
    need(proc.returncode == 0, "watch.py exit 0, got %r stderr %r" % (proc.returncode, proc.stderr))
    expected_line = "watch: v4.0.0/2025-01-23T19:00:03Z release_id 196495150 prerelease=False draft=False source=https://api.github.com/repos/Uniswap/v4-core/releases/latest"
    need(proc.stdout.strip() == expected_line, "watch.py stdout: %r" % (proc.stdout,))
    print(proc.stdout.strip())
    need("Caveats first" in readme and "UNTESTED" in readme and "python3 self_test.py" in readme, "README caveats/untested/command")
    need("watch.py" in readme, "README watch.py")
    need("v4.0.0" in readme and "2025-01-23T19:00:03Z" in readme, "README verified values")
    need("https://api.github.com/repos/Uniswap/v4-core/releases/latest" in readme, "README API URL")
    need("hivepunk-547-db38b7a4" in readme, "README HF namespace")
    print("README has caveats first, untested marks, command, verified values, HF namespace")
    need("seed_row.json" in art and "README.md" in art and "self_test.py" in art and "ARTIFACTS.md" in art, "ARTIFACTS list")
    need("python3 self_test.py" in art, "ARTIFACTS exact command")
    need("tools/uniswap-v4-upgrade-watch/" in art, "ARTIFACTS folder path")
    need("Raw stdout, stderr and exit code" in art, "ARTIFACTS verification output slot")
    need("NOT confirmed" in art and "Commit note" in art and "Left for owner" in art, "ARTIFACTS not-confirmed/commit-note/owner")
    need("self-test: all checks passed" in art and "exit code: 0" in art, "ARTIFACTS raw exit-0 output")
    need("seed_row.json: verified v4.0.0" in art, "ARTIFACTS raw stdout lines include verified")
    need("v4.0.0" in art and "2025-01-23T19:00:03Z" in art, "ARTIFACTS verified values")
    need("https://api.github.com/repos/Uniswap/v4-core/releases/latest" in art, "ARTIFACTS API URL")
    print("ARTIFACTS.md records artifacts, command, verification slot, NOT confirmed, commit note, left-for-owner")
    print("self-test: all checks passed")
    return 0
if __name__ == "__main__":
    sys.exit(main())
