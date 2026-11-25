#!/usr/bin/env python3
"""Offline post-publish byte-match checker for the two-file publish set.

Read-only. No network.

Usage:
  python3 verify_upload.py                 # list the publish set + checklist
  python3 verify_upload.py --json          # same, as JSON
  python3 verify_upload.py --remote DIR    # compare DIR's copies to local

For --remote DIR, DIR must hold raw downloads of the two files that keep
their repository paths, i.e. DIR/README.md and DIR/data/seed_row.json.
One line per file is printed: ok, MISSING or MISMATCH (with both hashes).
Exit 0 only when both files match byte-for-byte, 2 when a file is missing
or differs, 1 on a usage or IO error.
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import hf_manifest


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def check_remote(remote_dir, rel_list):
    rows = []
    ok = True
    for rel in rel_list:
        local = os.path.join(HERE, rel)
        remote = os.path.join(remote_dir, rel)
        local_hash = sha256_of(local)
        local_bytes = os.path.getsize(local)
        if not os.path.isfile(remote):
            ok = False
            rows.append("MISSING %s: not found at %s (local sha256=%s)" % (
                rel, remote, local_hash))
            continue
        remote_hash = sha256_of(remote)
        if remote_hash == local_hash:
            rows.append("ok %s: sha256=%s bytes=%d" % (
                rel, remote_hash, local_bytes))
        else:
            ok = False
            rows.append("MISMATCH %s: local sha256=%s remote sha256=%s" % (
                rel, local_hash, remote_hash))
    return rows, ok


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    remote_dir = None
    as_json = "--json" in argv
    if "--remote" in argv:
        i = argv.index("--remote")
        if i + 1 >= len(argv):
            sys.stderr.write("FAIL: --remote needs a directory\n")
            return 1
        remote_dir = argv[i + 1]
    try:
        manifest = hf_manifest.build_manifest()
    except Exception as e:
        sys.stderr.write("FAIL: %s\n" % e)
        return 1

    if remote_dir is not None:
        if not os.path.isdir(remote_dir):
            sys.stderr.write("FAIL: not a directory: %s\n" % remote_dir)
            return 1
        try:
            rel_list = [f["path"] for f in manifest["publish_files"]]
            rows, ok = check_remote(remote_dir, rel_list)
        except OSError as e:
            sys.stderr.write("FAIL: %s\n" % e)
            return 1
        for line in rows:
            print(line)
        if ok:
            print("match: both publish files are byte-identical to the local "
                  "sha256 values")
            return 0
        print("gap: remote does not match the local files; report the exact "
              "MISSING/MISMATCH line above and do not edit local files to "
              "please the remote")
        return 2

    payload = {
        "dataset_repo_id": manifest["dataset_repo_id"],
        "live_url": manifest["live_url"],
        "tree_url": manifest["live_url"] + "/tree/main",
        "publish_files": manifest["publish_files"],
        "usage": "download the raw files keeping paths into DIR, then run "
                 "python3 verify_upload.py --remote DIR",
        "card_render_check": [
            "open the live URL and confirm the README.md card renders",
            "open " + manifest["live_url"] + "/tree/main and confirm both files",
            "a single JSON object may show no table; the file is still "
            "downloadable",
        ],
        "untested": [
            "the publish itself (publish play, not this script)",
            "the live URL responding",
            "remote bytes and card rendering",
            "whether v4.0.0 is still latest at view time",
        ],
    }
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    print("dataset: %s" % payload["dataset_repo_id"])
    print("live: %s" % payload["live_url"])
    for f in payload["publish_files"]:
        print("  %s bytes=%s sha256=%s" % (
            f["path"], f["bytes"], f["sha256"]))
    print("then: python3 verify_upload.py --remote DIR")
    for line in payload["card_render_check"]:
        print("  check: " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
