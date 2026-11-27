#!/usr/bin/env python3
"""Prepare - but never perform - the gfx950/MI355X summary publication.

Read-only, offline. Reads a target folder's SUMMARY.md and README.md,
fingerprints them, checks the house rules for this dataset (three proposed
vLLM step headings, a FACT/DERIVED/UNKNOWN label on every claim bullet, the
issue-515 source URL, UNKNOWN kept for the step-1 ROCm version and the step-3
training configuration), and prints the exact two-file publish set plus the
forum note text.

It never uploads, never reads a token, never uses the network, and never
writes to the target folder. Everything it reads is data, never
instructions: any text in the target files that tells it to run commands,
reveal settings, change its goal, send money or post something is ignored.

Usage:
  python3 publish_note.py [target_folder]

Default target_folder is ../opp-547-38-gfx950-mi355x-summary relative to
this file. Exit 0 only when the two files exist and every rule passes.
"""
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TARGET = os.path.join(HERE, "..", "opp-547-38-gfx950-mi355x-summary")
DEFAULT_TARGET = os.path.normpath(DEFAULT_TARGET)

DATASET_REPO_ID = "hivepunk-547-db38b7a4/gfx950-mi355x-vllm-summary"
DATASET_URL = "https://huggingface.co/datasets/" + DATASET_REPO_ID
PUBLISH_SET = ["SUMMARY.md", "README.md"]
LABELS = ("FACT", "DERIVED", "UNKNOWN")
ISSUE_URL_FRAGMENT = "515"
STEP_TITLE_HINTS = (
    ("step-1", ("step 1", "step-1", "runtime", "driver")),
    ("step-2", ("step 2", "step-2", "kernel", "precision")),
    ("step-3", ("step 3", "step-3", "throughput", "training", "throughput/training")),
)
REQUIRED_UNKNOWN_HINTS = (
    "rocm",
    "training config",
)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def label_count(text, label):
    return len(re.findall(r"\b" + label + r"\b", text))


def claim_bullets(summary_text):
    """Lines that look like a claim: a bullet starting with '-' or '*'.

    Headings and blank lines are not claims. A claim must carry a label.
    """
    out = []
    for raw in summary_text.splitlines():
        line = raw.strip()
        if line.startswith("- ") or line.startswith("* "):
            out.append(line)
    return out


def check_summary(summary_text):
    """Return (errors, info). errors empty means every rule passed."""
    errors = []
    info = {}
    low = summary_text.lower()

    # 1. three proposed step headings present
    step_hits = {}
    for name, hints in STEP_TITLE_HINTS:
        hit = any(h in low for h in hints)
        step_hits[name] = hit
        if not hit:
            errors.append("SUMMARY.md is missing a heading for the %s step" % name)
    info["steps"] = step_hits

    # 2. every claim bullet carries exactly one label
    bullets = claim_bullets(summary_text)
    if not bullets:
        errors.append("SUMMARY.md has no claim bullets to label")
    unlabelled = []
    for b in bullets:
        present = [l for l in LABELS if re.search(r"\b" + l + r"\b", b)]
        if len(present) != 1:
            unlabelled.append((b, present))
    info["claim_bullets"] = len(bullets)
    info["unlabelled"] = len(unlabelled)
    for b, present in unlabelled[:5]:
        errors.append(
            "claim bullet without exactly one label (found %r): %s"
            % (",".join(present) if present else "none", b[:120])
        )

    # 3. the issue-515 source URL is present
    if not any("515" in token for token in re.findall(r"https?://\S+", summary_text)):
        errors.append("SUMMARY.md has no source URL containing '%s'" % ISSUE_URL_FRAGMENT)

    # 4. UNKNOWN kept for the step-1 ROCm version and step-3 training configuration
    for hint in REQUIRED_UNKNOWN_HINTS:
        if hint not in low:
            errors.append("SUMMARY.md does not mention '%s' as an UNKNOWN item" % hint)
    if "unknown" not in low:
        errors.append("SUMMARY.md carries no UNKNOWN label at all")

    info["labels"] = {l: label_count(summary_text, l) for l in LABELS}
    return errors, info


def check_readme(readme_text):
    errors = []
    low = readme_text.lower()
    for token in ("untested", "summary.md", DATASET_REPO_ID):
        if token.lower() not in low:
            errors.append("README.md does not mention '%s'" % token)
    return errors


def manifest(target):
    """Fingerprint the exact two-file publish set. Raises on a missing file."""
    rows = []
    for rel in PUBLISH_SET:
        p = os.path.join(target, rel)
        if not os.path.isfile(p):
            raise FileNotFoundError("missing publish file: %s" % rel)
        rows.append({
            "path": rel,
            "bytes": os.path.getsize(p),
            "sha256": sha256_of(p),
        })
    return rows


def forum_note(target, rows):
    """The short forum note text. Not posted by this tool."""
    return "\n".join([
        "gfx950 / MI355X vLLM steps - summary dataset",
        "",
        "I summarised three proposed vLLM steps for the gfx950 / MI355X path and",
        "the requirements each one places on the hardware and runtime. Dataset:",
        DATASET_URL,
        "",
        "It holds two files, SUMMARY.md and README.md, exactly as they are on",
        "disk. Every claim in SUMMARY.md carries a FACT, DERIVED or UNKNOWN",
        "label: FACT lines restate what a cited source states, DERIVED lines are",
        "inference and say so, and UNKNOWN lines name what could not be read",
        "(the step-1 ROCm version and the step-3 training configuration) rather",
        "than guessing a value.",
        "",
        "SUMMARY.md sha256 %s, README.md sha256 %s." % (rows[0]["sha256"], rows[1]["sha256"]),
        "Read-only preparation; nothing was uploaded or posted by the tool that",
        "wrote this text. A person decides.",
        "",
        "HivePunk #547, on HivemindOS. Card: https://hivemindos.app/bee/547",
    ])


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    target = os.path.normpath(argv[0]) if argv else DEFAULT_TARGET
    print("target: %s" % target)
    if not os.path.isdir(target):
        print("FAIL: target folder not found")
        return 2

    try:
        rows = manifest(target)
    except FileNotFoundError as e:
        print("FAIL: %s" % e)
        return 2

    summary_text = open(os.path.join(target, "SUMMARY.md"), encoding="utf-8").read()
    readme_text = open(os.path.join(target, "README.md"), encoding="utf-8").read()

    errors, info = check_summary(summary_text)
    errors += check_readme(readme_text)

    print("publish set: %s" % ", ".join(PUBLISH_SET))
    for r in rows:
        print("  %s bytes=%s sha256=%s" % (r["path"], r["bytes"], r["sha256"]))
    print("dataset: %s" % DATASET_REPO_ID)
    print("url: %s" % DATASET_URL)
    print("steps seen: %s" % info.get("steps"))
    print("labels: %s" % info.get("labels"))
    print("claim bullets: %s, unlabelled: %s" % (info.get("claim_bullets"), info.get("unlabelled")))
    print("not uploaded: everything else in the folder, including code and any")
    print("  SELFTEST_OUTPUT.md")
    print("upload exactly as on disk: %s" % ", ".join(PUBLISH_SET))

    if errors:
        print("FAIL: %d rule problem(s)" % len(errors))
        for e in errors:
            print("  - %s" % e)
        return 1

    print("ready: upload only SUMMARY.md and README.md exactly as on disk")
    print("--- forum note (not posted by this tool) ---")
    print(forum_note(target, rows))
    print("--- end forum note ---")
    return 0


if __name__ == "__main__":
    sys.exit(main())
