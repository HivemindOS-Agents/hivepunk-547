#!/usr/bin/env python3
"""Standalone self-test. No args, no network, run alone from this folder.

Imports and runs this folder's own watch.py and hf_manifest.py on
data/seed_row.json sample data and compares outputs to expected values.
"""
import hashlib, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import watch, hf_manifest
def fail(m):
    sys.stderr.write("FAIL: %s\n" % m); sys.exit(1)
def need(c, m):
    if not c:
        fail(m)
def sha(p):
    h = hashlib.sha256(); h.update(open(p, "rb").read()); return h.hexdigest()
def run(args):
    return subprocess.run([sys.executable] + args, capture_output=True, text=True, timeout=30, cwd=HERE)
def main():
    seed_path = os.path.join(HERE, "data", "seed_row.json")
    need(os.path.isfile(seed_path), "data/seed_row.json present")
    seed = json.load(open(seed_path, encoding="utf-8"))
    need(seed.get("repository") == "Uniswap/v4-core", "seed repository")
    need(seed.get("latest_release_tag") == "v4.0.0", "latest_release_tag v4.0.0")
    need(seed.get("latest_release_date") == "2025-01-23T19:00:03Z", "latest_release_date")
    need(seed.get("release_id") == 196495150, "release_id 196495150")
    need(seed.get("prerelease") is False and seed.get("draft") is False, "prerelease/draft false")
    need(seed.get("source_url") == "https://api.github.com/repos/Uniswap/v4-core/releases/latest", "source_url")
    summary = watch.load_seed(seed_path)
    expected = {"repository": "Uniswap/v4-core", "tag": "v4.0.0", "date": "2025-01-23T19:00:03Z", "release_id": 196495150, "prerelease": False, "draft": False, "source_url": "https://api.github.com/repos/Uniswap/v4-core/releases/latest"}
    need(summary == expected, "watch.load_seed output %r" % (summary,))
    print("watch.load_seed(data/seed_row.json): v4.0.0/2025-01-23T19:00:03Z release_id 196495150")
    p = run([os.path.join(HERE, "watch.py"), seed_path])
    need(p.returncode == 0, "watch.py exit %r %r" % (p.returncode, p.stderr))
    need(p.stdout.strip() == "watch: v4.0.0/2025-01-23T19:00:03Z release_id 196495150 prerelease=False draft=False source=https://api.github.com/repos/Uniswap/v4-core/releases/latest", "watch.py stdout %r" % (p.stdout,))
    print(p.stdout.strip())
    m = hf_manifest.build_manifest()
    need(m["dataset_repo_id"] == "hivepunk-547-db38b7a4/uniswap-v4-upgrade-watch", "manifest repo id")
    need(m["upload_exactly_as_on_disk"] == ["README.md", "data/seed_row.json"], "manifest upload list")
    need(m["seed"] == expected, "manifest seed")
    for entry in m["upload_files"]:
        fp = os.path.join(HERE, entry["path"])
        need(entry["bytes"] == os.path.getsize(fp), "manifest bytes " + entry["path"])
        need(entry["sha256"] == sha(fp), "manifest sha256 " + entry["path"])
    need("README.md" not in m["not_upload"] and "data/seed_row.json" not in m["not_upload"], "upload files not in not_upload")
    need("watch.py" in m["not_upload"] and "self_test.py" in m["not_upload"] and "hf_manifest.py" in m["not_upload"], "code files excluded from upload")
    print("hf_manifest.build_manifest(): upload README.md, data/seed_row.json with matching sha256")
    p = run([os.path.join(HERE, "hf_manifest.py"), "--check"])
    need(p.returncode == 0, "hf_manifest --check exit %r %r" % (p.returncode, p.stderr))
    need("ready: upload only README.md and data/seed_row.json exactly as on disk" in p.stdout, "hf_manifest --check output %r" % (p.stdout,))
    for line in p.stdout.strip().splitlines():
        print(line)
    p = run([os.path.join(HERE, "hf_manifest.py")])
    need(p.returncode == 0, "hf_manifest exit %r" % (p.returncode,))
    parsed = json.loads(p.stdout)
    need(parsed["dataset_repo_id"] == m["dataset_repo_id"] and parsed["upload_files"] == m["upload_files"], "hf_manifest JSON matches build_manifest")
    readme = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
    for s in ["Caveats first", "UNTESTED", "python3 self_test.py", "hivepunk-547-db38b7a4/uniswap-v4-upgrade-watch", "v4.0.0", "2025-01-23T19:00:03Z", "196495150", "hf_manifest.py"]:
        need(s in readme, "README contains " + s)
    print("README has caveats first, untested marks, command, verified values, HF repo")
    print("self-test: all checks passed")
    return 0
if __name__ == "__main__":
    sys.exit(main())
