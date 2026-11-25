#!/usr/bin/env python3
"""Standalone self-test. No args, no network, run alone from this folder.

Imports and runs this folder's own watch.py, hf_manifest.py and
verify_upload.py on data/seed_row.json sample data, and compares their
output to expected values, including a temp dir that must match, one
that must MISMATCH and one that must MISSING.
"""
import hashlib, json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import watch, hf_manifest, verify_upload

EXPECTED = {
    "repository": "Uniswap/v4-core",
    "tag": "v4.0.0",
    "date": "2025-01-23T19:00:03Z",
    "release_id": 196495150,
    "prerelease": False,
    "draft": False,
    "source_url": "https://api.github.com/repos/Uniswap/v4-core/releases/latest",
}


def fail(msg):
    sys.stderr.write("FAIL: %s\n" % msg)
    sys.exit(1)


def need(cond, msg):
    if not cond:
        fail(msg)


def sha(path):
    h = hashlib.sha256()
    h.update(open(path, "rb").read())
    return h.hexdigest()


def run(args):
    return subprocess.run([sys.executable] + args, capture_output=True,
                          text=True, timeout=60, cwd=HERE)


def copy_set(dest):
    for rel in hf_manifest.UPLOAD:
        src = os.path.join(HERE, rel)
        dst = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)


def main():
    seed_path = os.path.join(HERE, "data", "seed_row.json")
    need(os.path.isfile(seed_path), "data/seed_row.json present")
    seed = json.load(open(seed_path, encoding="utf-8"))
    need(seed.get("repository") == "Uniswap/v4-core", "seed repository")
    need(seed.get("latest_release_tag") == "v4.0.0", "latest_release_tag")
    need(seed.get("latest_release_date") == "2025-01-23T19:00:03Z", "date")
    need(seed.get("release_id") == 196495150, "release_id")
    need(seed.get("prerelease") is False and seed.get("draft") is False,
         "prerelease/draft false")

    summary = watch.load_seed(seed_path)
    need(summary == EXPECTED, "watch.load_seed output %r" % (summary,))
    print("watch.load_seed(data/seed_row.json): v4.0.0/2025-01-23T19:00:03Z "
          "release_id 196495150")

    p = run([os.path.join(HERE, "watch.py"), seed_path])
    need(p.returncode == 0, "watch.py exit %r %r" % (p.returncode, p.stderr))
    want = ("watch: v4.0.0/2025-01-23T19:00:03Z release_id 196495150 "
            "prerelease=False draft=False "
            "source=https://api.github.com/repos/Uniswap/v4-core/releases/latest")
    need(p.stdout.strip() == want, "watch.py stdout %r" % (p.stdout,))
    print(p.stdout.strip())

    m = hf_manifest.build_manifest()
    need(m["dataset_repo_id"] ==
         "hivepunk-547-db38b7a4/uniswap-v4-upgrade-watch", "manifest repo id")
    need(m["upload_exactly_as_on_disk"] == ["README.md", "data/seed_row.json"],
         "manifest upload list")
    need(m["seed"] == EXPECTED, "manifest seed")
    for entry in m["upload_files"]:
        fp = os.path.join(HERE, entry["path"])
        need(entry["bytes"] == os.path.getsize(fp),
             "manifest bytes " + entry["path"])
        need(entry["sha256"] == sha(fp), "manifest sha256 " + entry["path"])
    need("README.md" not in m["not_upload"] and
         "data/seed_row.json" not in m["not_upload"],
         "upload files not in not_upload")
    need("watch.py" in m["not_upload"] and "self_test.py" in m["not_upload"]
         and "hf_manifest.py" in m["not_upload"],
         "code files excluded from upload")
    print("hf_manifest.build_manifest(): upload README.md, data/seed_row.json "
          "with matching sha256")

    src = open(os.path.join(HERE, "verify_upload.py"), encoding="utf-8").read()
    need("HF_TOKEN" not in src, "verify_upload.py must not mention HF_TOKEN")
    need("huggingface_hub" not in src,
         "verify_upload.py must not import huggingface_hub")
    need("upload_file" not in src and "create_repo" not in src,
         "verify_upload.py must not contain upload code")
    print("verify_upload.py is offline: no token, no huggingface_hub, no upload")

    with tempfile.TemporaryDirectory() as tmp:
        copy_set(tmp)
        p = run([os.path.join(HERE, "verify_upload.py"), "--remote", tmp])
        need(p.returncode == 0, "matching dir exit %r %r" % (p.returncode, p.stdout))
        need(p.stdout.count("ok ") == 2 and "MISSING" not in p.stdout
             and "MISMATCH" not in p.stdout,
             "matching dir output %r" % (p.stdout,))
        need("match: both upload files are byte-identical" in p.stdout,
             "matching dir summary line")
        print("verify_upload.py --remote on byte-identical copies: exit 0, both ok")

        rp = os.path.join(tmp, "README.md")
        with open(rp, "ab") as f:
            f.write(b"x")
        p = run([os.path.join(HERE, "verify_upload.py"), "--remote", tmp])
        need(p.returncode == 2, "mismatch exit %r" % (p.returncode,))
        need("MISMATCH README.md" in p.stdout, "mismatch line %r" % (p.stdout,))
        print(p.stdout.strip().splitlines()[0])

        copy_set(tmp)  # restore README, then drop the seed row
        os.remove(os.path.join(tmp, "data", "seed_row.json"))
        p = run([os.path.join(HERE, "verify_upload.py"), "--remote", tmp])
        need(p.returncode == 2, "missing exit %r" % (p.returncode,))
        need("MISSING data/seed_row.json" in p.stdout,
             "missing line %r" % (p.stdout,))
        print("MISSING data/seed_row.json: reported as MISSING, exit 2")

    p = run([os.path.join(HERE, "verify_upload.py"), "--json"])
    need(p.returncode == 0, "listing exit %r" % (p.returncode,))
    listed = json.loads(p.stdout)
    need(listed["upload_files"] == m["upload_files"],
         "listing upload files match manifest")
    need(listed["dataset_repo_id"] == m["dataset_repo_id"], "listing repo id")
    print("verify_upload.py listing: two-file publish set with sha256")

    readme = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
    for s in ["Caveats first", "UNTESTED", "python3 self_test.py",
              "hivepunk-547-db38b7a4/uniswap-v4-upgrade-watch", "v4.0.0",
              "2025-01-23T19:00:03Z", "196495150", "hf_manifest.py"]:
        need(s in readme, "README contains " + s)
    print("README has caveats first, untested marks, command, verified values, HF repo")

    print("self-test: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
