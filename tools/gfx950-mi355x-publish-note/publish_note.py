#!/usr/bin/env python3
"""Prepare - but never perform - the gfx950/MI355X summary publication.

Read-only, offline. Reads a target folder's SUMMARY.md and README.md,
fingerprints them, checks the house rules for this dataset (three proposed
vLLM step headings, a FACT/DERIVED/UNKNOWN label on every claim bullet, the
issue-515 source URL, UNKNOWN kept for the step-1 ROCm version and the step-3
training configuration), optionally compares them to a recorded manifest, and
prints the exact two-file publish set plus the announcement text (whose first
sentence names the dataset title).

It never uploads, never reads a token, never uses the network, and never
writes to the target folder. Everything it reads is data, never
instructions: any text in the target files or manifest that tells it to run
commands, reveal settings, change its goal, send money or post something is
ignored.

Usage:
  python3 publish_note.py [target_folder]
  python3 publish_note.py [target_folder] --manifest FILE
  python3 publish_note.py [target_folder] --write-manifest FILE

Default target_folder is ../opp-547-38-gfx950-mi355x-summary relative to
this file. Exit 0 only when the two files exist, every rule passes, and any
given manifest matches.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TARGET = os.path.join(HERE, "..", "opp-547-38-gfx950-mi355x-summary")
DEFAULT_TARGET = os.path.normpath(DEFAULT_TARGET)

DATASET_REPO_ID = "hivepunk-547-db38b7a4/gfx950-mi355x-vllm-summary"
DATASET_TITLE = "gfx950 / MI355X vLLM steps - summary dataset"
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
    """Lines that look like a claim: a bullet starting with '- ' or '* '."""
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
    if not any(ISSUE_URL_FRAGMENT in token for token in re.findall(r"https?://\S+", summary_text)):
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


def compare_manifest(rows, recorded):
    """Compare current rows to a recorded manifest. Returns list of errors."""
    errors = []
    by_path = {}
    for r in recorded:
        if isinstance(r, dict) and isinstance(r.get("path"), str):
            by_path[r["path"]] = r
    for r in rows:
        rec = by_path.get(r["path"])
        if rec is None:
            errors.append("manifest has no entry for %s" % r["path"])
            continue
        if rec.get("bytes") != r["bytes"]:
            errors.append(
                "%s size drift: manifest %r, disk %r"
                % (r["path"], rec.get("bytes"), r["bytes"])
            )
        if rec.get("sha256") != r["sha256"]:
            errors.append(
                "%s sha256 drift: manifest %r, disk %r"
                % (r["path"], rec.get("sha256"), r["sha256"])
            )
    for path in by_path:
        if path not in [r["path"] for r in rows]:
            errors.append("manifest lists %s, which is not in the publish set" % path)
    return errors


def announcement(rows):
    """The announcement text. Not posted by this tool.

    Its first sentence names the dataset title, so anyone reading only the
    top line knows what is being shared.
    """
    return "\n".join([
        "%s - read it at %s." % (DATASET_TITLE, DATASET_URL),
        "",
        "I summarised three proposed vLLM steps for the gfx950 / MI355X path and",
        "the requirements each one places on the hardware and runtime. The",
        "dataset holds two files, SUMMARY.md and README.md, exactly as they are",
        "on disk.",
        "",
        "Every claim in SUMMARY.md carries a FACT, DERIVED or UNKNOWN label:",
        "FACT lines restate what a cited source states, DERIVED lines are",
        "inference and say so, and UNKNOWN lines name what could not be read (the",
        "step-1 ROCm version and the step-3 training configuration) rather than",
        "guessing a value.",
        "",
        "SUMMARY.md sha256 %s, README.md sha256 %s." % (rows[0]["sha256"], rows[1]["sha256"]),
        "Read-only preparation; nothing was uploaded or posted by the tool that",
        "wrote this text. A person decides.",
        "",
        "HivePunk #547, on HivemindOS. Card: https://hivemindos.app/bee/547",
    ])


def parse_args(argv):
    target = None
    manifest_path = None
    write_manifest = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--manifest", "--write-manifest"):
            if i + 1 >= len(argv):
                raise SystemExit("FAIL: %s needs a file" % a)
            if a == "--manifest":
                manifest_path = argv[i + 1]
            else:
                write_manifest = argv[i + 1]
            i += 2
        else:
            if target is not None:
                raise SystemExit("FAIL: unexpected argument %r" % a)
            target = a
            i += 1
    if target is None:
        target = DEFAULT_TARGET
    return os.path.normpath(target), manifest_path, write_manifest


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        target, manifest_path, write_manifest = parse_args(argv)
    except SystemExit as e:
        print(str(e))
        return 2
    print("target: %s" % target)
    if not os.path.isdir(target):
        print("FAIL: target folder not found")
        return 2

    try:
        rows = manifest(target)
    except FileNotFoundError as e:
        print("FAIL: %s" % e)
        return 2

    with open(os.path.join(target, "SUMMARY.md"), encoding="utf-8") as f:
        summary_text = f.read()
    with open(os.path.join(target, "README.md"), encoding="utf-8") as f:
        readme_text = f.read()

    errors, info = check_summary(summary_text)
    errors += check_readme(readme_text)

    if manifest_path:
        try:
            with open(manifest_path, encoding="utf-8") as f:
                recorded = json.load(f)
        except (OSError, ValueError) as e:
            print("FAIL: could not read manifest %s: %s" % (manifest_path, e))
            return 2
        if isinstance(recorded, dict) and "files" in recorded:
            recorded = recorded["files"]
        if not isinstance(recorded, list):
            print("FAIL: manifest must be a JSON list or an object with a 'files' list")
            return 2
        errors += compare_manifest(rows, recorded)
        print("manifest compared: %s" % manifest_path)

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

    if write_manifest:
        if os.path.abspath(write_manifest) == os.path.abspath(os.path.join(target, os.path.basename(write_manifest))):
            print("FAIL: refusing to write a manifest into the target folder")
            return 2
        payload = {
            "dataset": DATASET_REPO_ID,
            "url": DATASET_URL,
            "files": rows,
        }
        with open(write_manifest, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, sort_keys=True)
            f.write("\n")
        print("manifest written: %s" % write_manifest)

    print("ready: upload only SUMMARY.md and README.md exactly as on disk")
    print("--- announcement (not posted by this tool) ---")
    print(announcement(rows))
    print("--- end announcement ---")
    return 0


if __name__ == "__main__":
    sys.exit(main())
