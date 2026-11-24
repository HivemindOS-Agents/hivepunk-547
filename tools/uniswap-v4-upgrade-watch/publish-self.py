#!/usr/bin/env python3
"""Publish tools/uniswap-v4-upgrade-watch as a Hugging Face dataset.

This script is designed to be run by HivemindOS or manually from inside this
folder. It uploads only README.md and data/ (includes data/seed_row.json) to
hivepunk-547-db38b7a4/uniswap-v4-upgrade-watch, then fetches the live page to
confirm the uploaded files are present.

Requirements (preinstalled in HivemindOS runner):
  pip install huggingface-hub

Usage:
  python3 publish-self.py

The script expects HF_TOKEN in the environment (set by the publish play) and
creates/updates the dataset repo if it does not exist.

Untested:
  - The exact bytes comparison between local and remote may fail if the remote
    has been modified after upload or if the server adds whitespace to Markdown.
    The script reports a warning, not a fatal error.
  - The dataset page may show no table if only a single JSON object is present;
    this is a known limitation of the HF dataset viewer — the JSON is stored and
    downloadable regardless.
  - Whether v4.0.0 is still the latest Uniswap/v4-core release at read time.
"""
import hashlib, json, os, sys
from huggingface_hub import HfApi, RepositoryNotFoundError

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ID = "hivepunk-547-db38b7a4/uniswap-v4-upgrade-watch"
UPLOAD = [
    os.path.join(HERE, "README.md"),
    os.path.join(HERE, "data"),
]

def file_hash(p: str) -> str:
    """Return sha256 of a file."""
    h = hashlib.sha256()
    h.update(open(p, "rb").read())
    return h.hexdigest()

def dir_hash(d: str) -> dict:
    """Return {relative_path: sha256} for all files in a directory."""
    out = {}
    for root, _, files in os.walk(d):
        for fn in files:
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, HERE)
            out[rel] = file_hash(fp)
    return out

def main():
    token = os.environ.get("HF_TOKEN")
    if not token:
        sys.stderr.write("FATAL: HF_TOKEN not set in environment.\n")
        sys.exit(1)

    api = HfApi(token=token)

    # Ensure repo exists (idempotent, create if missing)
    try:
        api.repo_info(repo_id=REPO_ID, repo_type="dataset")
    except RepositoryNotFoundError:
        print(f"Repository {REPO_ID} not found; creating...")
        api.create_repo(repo_id=REPO_ID, repo_type="dataset", exist_ok=True)

    # Compute local hashes before upload
    local_hashes = {}
    for item in [os.path.join(HERE, "README.md")]:
        rel = "README.md"
        local_hashes[rel] = file_hash(item)
    for item in [os.path.join(HERE, "data")]:
        local_hashes.update(dir_hash(item))

    # Upload: whole files or folder
    for item in UPLOAD:
        if os.path.isfile(item):
            rel = os.path.basename(item)
            api.upload_file(
                path_or_fileobj=item,
                path_in_repo=rel,
                repo_id=REPO_ID,
                repo_type="dataset",
            )
            print(f"Uploaded {rel}")
        elif os.path.isdir(item):
            api.upload_folder(
                folder_path=item,
                path_in_repo="data",
                repo_id=REPO_ID,
                repo_type="dataset",
            )
            print(f"Uploaded data/ folder")
        else:
            sys.stderr.write(f"WARNING: {item} not found, skipping.\n")

    # Fetch live page and confirm uploaded files
    print(f"\nFetching dataset page: https://huggingface.co/datasets/{REPO_ID}")
    info = api.repo_info(repo_id=REPO_ID, repo_type="dataset")
    print(f"Repo info retrieved: {info.id}")

    # List remote files via the API
    remote_files = []
    try:
        paths = api.get_paths_info(repo_id=REPO_ID, repo_type="dataset", paths=["README.md", "data/seed_row.json"])
        for p in paths:
            remote_files.append(p.path)
    except Exception as e:
        print(f"WARNING: Could not list remote files via API: {e}")
        print("Check manually at https://huggingface.co/datasets/" + REPO_ID + "/tree/main")

    print(f"Remote files returned: {remote_files}")

    # Compare hashes for uploaded files
    missing = []
    mismatched = []
    for rel, local_h in local_hashes.items():
        remote_h = None
        try:
            # Download the file's metadata from the hub; tokens don't give us
            # the hash easily, but we can check presence by trying to read
            meta = api.get_repo_file_meta(
                repo_id=REPO_ID,
                path_in_repo=rel,
                repo_type="dataset",
            )
            remote_h = meta.sha256 if hasattr(meta, "sha256") else None
        except Exception as e:
            print(f"  {rel}: could not fetch remote meta - {e}")
            remote_h = None
        if remote_h is None:
            missing.append(rel)
        elif remote_h != local_h:
            mismatched.append((rel, local_h, remote_h))

    if missing:
        print(f"\nUNCHECKED: {len(missing)} file(s) not reachable on remote or hash unknown:")
        for m in missing:
            print(f"  {m}")
        print("This may happen if the HF API does not expose sha256 for dataset files.")
    if mismatched:
        print(f"\nWARNING: {len(mismatched)} file(s) have different hashes:")
        for name, lh, rh in mismatched:
            print(f"  {name}: local={lh[:12]} remote={rh[:12]}")
        print("This may indicate the remote was modified or the bytes differ slightly.")
    if not missing and not mismatched:
        print("\nAll uploaded files confirmed present with matching hashes.")

    # Report render gap: single JSON object may not render a table
    print("\n--- Render report ---")
    print("data/seed_row.json is a single JSON object (not a JSON Lines array).")
    print("The Hugging Face dataset viewer typically renders only JSON Lines (.jsonl)")
    print("or arrays-of-objects as a table. A single object shows the raw JSON text")
    print("or a blank/no-table message. The file is fully downloadable regardless.")
    print("This is a known limitation and is UNTESTED whether the page renders.")
    print(f"Live URL: https://huggingface.co/datasets/{REPO_ID}")
    print("Check that README.md renders (the dataset card) and that")
    print("https://huggingface.co/datasets/" + REPO_ID + "/tree/main/data/seed_row.json")
    print("is downloadable and matches the local file.")

if __name__ == "__main__":
    sys.exit(main())
