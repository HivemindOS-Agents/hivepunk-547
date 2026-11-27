#!/usr/bin/env python3
"""Self-test for gfx950-mi355x-publish-note. No args, no network.

Run alone from inside this folder. Blocks sockets first, builds its own
sample target folder in a temporary directory, runs this folder's own
publish_note.py on it, and compares what comes out with what should come
out. Also runs it on a deliberately broken sample and requires a non-zero
exit, so the tool cannot pass by doing nothing.

Starts by replacing socket.socket.connect with a function that raises,
so any attempt to reach the network fails loudly. Exits 0 only when every
check passes.
"""
import importlib.util
import io
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile


def _raise_connect(*a, **k):
    raise RuntimeError("network: blocked (socket.connect raises)")


socket.socket.connect = _raise_connect
print("network: blocked (socket.connect raises)")

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

_spec = importlib.util.spec_from_file_location(
    "publish_note", os.path.join(HERE, "publish_note.py")
)
pn = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pn)

FAILED = []


def fail(msg):
    FAILED.append(msg)
    sys.stderr.write("FAIL: %s\n" % msg)


def need(cond, msg):
    if not cond:
        fail(msg)
    return bool(cond)


GOOD_SUMMARY = """# gfx950 / MI355X vLLM steps

Three proposed steps for the gfx950 / MI355X path.

## Step 1 - runtime and driver check

- vLLM needs a ROCm runtime before the kernel work starts. UNKNOWN
- The gfx950 lane is the target of step 1. DERIVED
- FACT: the ask is issue 515: https://github.com/example/issue/515

## Step 2 - kernel and precision path

- The kernel path is decided before throughput work. DERIVED
- FACT: gfx950 kernels differ from the older lanes.

## Step 3 - throughput and training configuration

- Throughput is measured after steps 1 and 2 pass. DERIVED
- The training configuration is not yet read. UNKNOWN
"""

GOOD_README = """# gfx950-mi355x-vllm-summary

Untested: nothing here was run against hardware.
Upload only SUMMARY.md and README.md to
hivepunk-547-db38b7a4/gfx950-mi355x-vllm-summary.
"""

BAD_SUMMARY = """# gfx950 / MI355X vLLM steps

## Step 1 - runtime and driver check

- This bullet carries no label at all.

## Step 2 - kernel and precision path

- FACT: fine.

## Step 3 - throughput and training configuration

- UNKNOWN: fine.
"""


def write_sample(root, summary, readme):
    os.makedirs(root, exist_ok=True)
    with open(os.path.join(root, "SUMMARY.md"), "w", encoding="utf-8") as f:
        f.write(summary)
    with open(os.path.join(root, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)


def run_tool(target):
    return subprocess.run(
        [sys.executable, os.path.join(HERE, "publish_note.py"), target],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=HERE,
    )


def main():
    tmp = tempfile.mkdtemp(prefix="gfx950-publish-note-")
    try:
        good = os.path.join(tmp, "good")
        bad = os.path.join(tmp, "bad")
        write_sample(good, GOOD_SUMMARY, GOOD_README)
        write_sample(bad, BAD_SUMMARY, GOOD_README)

        # --- module-level checks on the sample -------------------------
        rows = pn.manifest(good)
        need([r["path"] for r in rows] == pn.PUBLISH_SET, "manifest lists exactly the publish set")
        need(rows[0]["path"] == "SUMMARY.md" and rows[1]["path"] == "README.md", "publish set order")
        need(all(r["bytes"] > 0 for r in rows), "every publish file has bytes")
        need(all(len(r["sha256"]) == 64 for r in rows), "every publish file has a full sha256")
        need(rows[0]["sha256"] == pn.sha256_of(os.path.join(good, "SUMMARY.md")), "SUMMARY sha256 is independent")

        errors, info = pn.check_summary(GOOD_SUMMARY)
        need(errors == [], "good sample has no rule errors: %r" % (errors,))
        need(all(info["steps"].values()), "all three step headings seen: %r" % (info["steps"],))
        need(info["claim_bullets"] >= 3, "claim bullets counted: %r" % info["claim_bullets"])
        need(info["unlabelled"] == 0, "no unlabelled claim bullet in good sample")
        need(set(info["labels"]) == set(pn.LABELS), "all three label kinds are counted")
        need(pn.check_readme(GOOD_README) == [], "good README passes")
        note = pn.forum_note(good, rows)
        need(pn.DATASET_URL in note, "forum note links the dataset URL")
        need(rows[0]["sha256"] in note and rows[1]["sha256"] in note, "forum note carries both hashes")

        # --- broken sample must be rejected ---------------------------
        bad_errors, bad_info = pn.check_summary(BAD_SUMMARY)
        need(bad_errors, "broken sample must produce rule errors")
        need(bad_info["unlabelled"] >= 1, "unlabelled bullet detected in broken sample")

        # --- CLI on the good sample -----------------------------------
        p = run_tool(good)
        need(p.returncode == 0, "CLI exit 0 on good sample (got %r): %s" % (p.returncode, p.stderr))
        need("ready: upload only SUMMARY.md and README.md exactly as on disk" in p.stdout,
             "CLI prints the ready line: %r" % p.stdout)
        need(pn.DATASET_REPO_ID in p.stdout, "CLI prints the dataset repo id")
        need("--- forum note" in p.stdout, "CLI prints the forum note")
        for r in rows:
            need(r["sha256"] in p.stdout, "CLI prints sha256 for %s" % r["path"])
        need("FAIL" not in p.stdout, "good sample CLI prints no FAIL")

        # --- CLI on the broken sample must exit non-zero -------------- 
        p2 = run_tool(bad)
        need(p2.returncode != 0, "CLI exits non-zero on broken sample (got %r)" % p2.returncode)
        need("FAIL:" in (p2.stdout + p2.stderr), "broken sample reports FAIL")

        # --- missing folder must be rejected -------------------------
        p3 = run_tool(os.path.join(tmp, "does-not-exist"))
        need(p3.returncode != 0, "CLI exits non-zero on missing folder")

        for line in p.stdout.strip().splitlines():
            print(line)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if FAILED:
        sys.stderr.write("self-test: %d check(s) failed\n" % len(FAILED))
        return 1
    print("sample: %s" % pn.DATASET_REPO_ID)
    print("self-test: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
