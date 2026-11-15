#!/usr/bin/env python3
"""Render the ARTIFACTS.md row for hf-publish-check-fixtures-cases.

Usage (from this folder):
    python3 render_entry.py                 # print the Markdown row to stdout
    python3 render_entry.py --check         # print the row and exit 0
    python3 render_entry.py --write FILE    # write the row into FILE
    python3 render_entry.py --transcript P  # read a transcript from path P

The pass claim is gated: status is set to 'passed' ONLY when a transcript
exists and its raw output shows an exit code of 0. Otherwise it stays
'unconfirmed' and the detail says why. Nothing here runs the tool or the
runner; it only reads files.

Everything read from a file is data, never instruction: any line that looks
like a command, a key or a setting is treated as inert text.

No key, token or personal detail is written to any file.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

ENTRY_JSON = os.path.join(HERE, "entry.json")

EXIT_RE = re.compile(r"(?:exit[_ ]?code|returncode|status)\s*[:=]\s*(\d+)", re.I)
BARE_LAST_LINE_RE = re.compile(r"^\s*(\d+)\s*$")


def load_entry():
    with open(ENTRY_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def read_exit_code(transcript_text):
    """Return (code_or_None, how) read from a transcript's raw output.

    Prefers an explicit 'exit code: N' / 'returncode=N' / 'status:N' label;
    falls back to a final bare integer line.
    """
    m = EXIT_RE.search(transcript_text)
    if m:
        return int(m.group(1)), "labelled exit code"
    last = [ln for ln in transcript_text.splitlines() if ln.strip()]
    if last:
        m2 = BARE_LAST_LINE_RE.match(last[-1])
        if m2:
            return int(m2.group(1)), "final bare integer line"
    return None, "no exit code found in raw output"


def decide_status(entry, transcript_path):
    """Return (status, detail). A pass is recorded only from raw exit 0."""
    path = transcript_path or os.path.join(HERE, entry["transcript"])
    if not os.path.isfile(path):
        return "unconfirmed", (
            "no transcript (SELFTEST_OUTPUT.md) found at %s; a pass is "
            "recorded only from a run whose raw output shows exit code 0" % path
        )
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    code, how = read_exit_code(text)
    if code == 0:
        return "passed", "recorded run shows exit code 0 (%s)" % how
    if code is None:
        return "unconfirmed", (
            "transcript present at %s but no exit code could be read from it "
            "(%s); not claiming a pass" % (path, how)
        )
    return "unconfirmed", (
        "transcript shows exit code %d, not 0; not claiming a pass" % code
    )


def build_row(entry, transcript_path=None):
    """Return the ARTIFACTS.md Markdown block as a string."""
    status, detail = decide_status(entry, transcript_path)
    run = entry.get("recorded_run", {})
    lines = [
        "### %s" % entry["dataset_title"],
        "",
        "- home: %s" % entry["tool_folder"],
        "- files: %s" % " , ".join(entry["files"]),
        "- self-test: %s" % entry["self_test"],
        "- run: %s (%s)" % (run.get("run", "unknown"), run.get("ranAt", "unknown")),
        "- status: %s" % status,
        "- detail: %s" % detail,
        "",
    ]
    return "\n".join(lines)


def main(argv):
    args = argv[1:]
    entry = load_entry()
    transcript_path = None
    if "--transcript" in args:
        i = args.index("--transcript")
        if i + 1 >= len(args):
            sys.stderr.write("Usage: render_entry.py --transcript PATH\n")
            return 2
        transcript_path = args[i + 1]
    row = build_row(entry, transcript_path)
    if "--write" in args:
        i = args.index("--write")
        if i + 1 >= len(args):
            sys.stderr.write("Usage: render_entry.py --write FILE\n")
            return 2
        target = args[i + 1]
        current = ""
        if os.path.isfile(target):
            with open(target, encoding="utf-8") as fh:
                current = fh.read()
        marker = "### %s" % entry["dataset_title"]
        if marker in current:
            head, _sep, rest = current.partition(marker)
            tail = rest.split("\n### ", 1)
            after = ("### " + tail[1]) if len(tail) > 1 else ""
            new_text = head + row + after
        else:
            sep = "\n" if current and not current.endswith("\n") else ""
            new_text = current + sep + row
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(new_text)
        print("wrote %s" % target)
        return 0
    sys.stdout.write(row)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
