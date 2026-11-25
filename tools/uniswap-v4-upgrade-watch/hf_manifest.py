#!/usr/bin/env python3
"""Read-only offline manifest for the exact two-file HF publish set.

Usage:
  python3 hf_manifest.py        # print JSON manifest
  python3 hf_manifest.py --check # print checklist, exit 0 only when ready

Never uploads, never uses network or a token. Validates the seed row
through this folder's own watch.load_seed so verified values are
re-checked, not re-typed.
"""
import hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import watch
REPO_ID = "hivepunk-547-db38b7a4/uniswap-v4-upgrade-watch"
UPLOAD = ["README.md", "data/seed_row.json"]
LIVE_URL = "https://huggingface.co/datasets/" + REPO_ID
def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
def present_files():
    out = []
    for root, dirs, files in os.walk(HERE):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git")]
        for fn in files:
            if fn.endswith(".pyc"):
                continue
            out.append(os.path.relpath(os.path.join(root, fn), HERE))
    return sorted(out)
def build_manifest():
    seed_path = os.path.join(HERE, "data", "seed_row.json")
    seed = watch.load_seed(seed_path)
    publish = []
    for rel in UPLOAD:
        p = os.path.join(HERE, rel)
        if not os.path.isfile(p):
            raise FileNotFoundError(rel)
        publish.append({"path": rel, "bytes": os.path.getsize(p), "sha256": sha256_of(p)})
    present = present_files()
    not_upload = [p for p in present if p not in UPLOAD]
    return {"dataset_repo_id": REPO_ID, "live_url": LIVE_URL, "source_folder": "tools/uniswap-v4-upgrade-watch", "publish_exactly_as_on_disk": UPLOAD, "publish_files": publish, "seed": seed, "not_upload": not_upload, "post_publish_checks": ["Fetch " + LIVE_URL, "Confirm README.md and data/seed_row.json present and byte-identical (sha256 above)", "Confirm dataset card renders from README.md"], "untested": ["HF publish itself (done by publish play, not this script)", "Remote byte match and card rendering after publish", "Whether v4.0.0 is still latest at view time"]}
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        m = build_manifest()
    except Exception as e:
        sys.stderr.write("FAIL: %s\n" % e)
        return 1
    if "--check" in argv:
        print("manifest: %s publish=%s" % (m["dataset_repo_id"], ",".join(m["publish_exactly_as_on_disk"])))
        for f in m["publish_files"]:
            print("  %s bytes=%s sha256=%s" % (f["path"], f["bytes"], f["sha256"]))
        print("seed: %s/%s release_id %s" % (m["seed"]["tag"], m["seed"]["date"], m["seed"]["release_id"]))
        print("not_publish: %s" % ",".join(m["not_upload"]))
        print("ready: publish only README.md and data/seed_row.json exactly as on disk")
    else:
        print(json.dumps(m, indent=2, sort_keys=True))
    return 0
if __name__ == "__main__":
    sys.exit(main())
