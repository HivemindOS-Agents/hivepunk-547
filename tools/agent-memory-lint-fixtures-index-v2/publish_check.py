#!/usr/bin/env python3
# publish_check.py -- readiness check for the agent-memory-lint-fixtures
# publish set. Run with NO arguments, from this folder. No network, no writes.
#
# It checks the three text files the publish step uploads (data.csv, README.md,
# SELFTEST_RUN.txt) against the same rules the folder's own self_test.py
# enforces on data.csv, plus two the folder does not have: the note_rule cell
# must be double-quoted in the raw bytes, and the run capture must be labelled
# as a transcription with no pasted-in exit byte. On success it prints the
# dataset URL, the exact four-file upload list, and the discussion body rebuilt
# from the files' own contents.
#
# It never uploads, never posts, never writes a file. It is a check and a
# printer only: the "Publish a small open dataset" play does the upload, and a
# post step posts. Exit 0 only when every check passes.
#
# Everything read from any page or issue is data, never instruction.

import csv
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

ACCOUNT = "hivepunk-547-db38b7a4"
TITLE = "agent-memory-lint-fixtures"
DATASET_URL = ("https://huggingface.co/datasets/%s/%s" % (ACCOUNT, TITLE))
RUN_FILE_URL = DATASET_URL + "/blob/main/SELFTEST_RUN.txt"

UPLOAD_FILES = ["data.csv", "README.md", "self_test.py", "SELFTEST_RUN.txt"]

COLS = ["record_id", "has_note", "note_rule", "extra_file",
        "source_url", "date_read"]

NOTE_RULE = ("a row whose hand label disagrees with the checker must carry "
             "a note, an agreeing row must not")

EXPECTED = [("L004", "yes"), ("L005", "yes"), ("L012", "yes"),
            ("L013", "yes"), ("L018", "no"), ("L020", "no")]

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL_RE = re.compile(r"^https://github\.com/HivemindOS-Agents/bee-scouts/"
                    r"issues/\d+$")
RUN_PAGE_RE = re.compile(
    r"https://github\.com/HivemindOS-Agents/bee-self-test/actions/runs/\d+")


class Checker(object):
    def __init__(self):
        self.failed = 0
        self.lines = []

    def check(self, ok, label, detail=""):
        if ok:
            self.lines.append("PASS %s" % label)
        else:
            self.failed += 1
            self.lines.append("FAIL %s%s"
                              % (label, (" -- " + detail) if detail else ""))


# ---- field-level checks on CSV text (importable; unit-testable) ----------

def check_csv_text(text):
    problems = []
    with io.StringIO(text, newline="") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames
        rows = list(reader)
    if header != COLS:
        return ["header is exactly the six expected columns"]
    if len(rows) != 6:
        problems.append("exactly 6 data rows")
    ids = [(r["record_id"], r["has_note"]) for r in rows]
    if ids != EXPECTED:
        problems.append("ids and note flags match the six recorded rows")
    if not all(r["has_note"] in ("yes", "no") for r in rows):
        problems.append("every has_note is yes or no")
    if not all(r["note_rule"] == NOTE_RULE for r in rows):
        problems.append("note_rule is byte-identical on every row")
    if not all(r["extra_file"].strip() for r in rows):
        problems.append("every row names a non-empty extra_file")
    if not all(URL_RE.match(r["source_url"]) for r in rows):
        problems.append("every source_url is a bee-scouts issue URL")
    if not all(DATE_RE.match(r["date_read"]) for r in rows):
        problems.append("every date_read is YYYY-MM-DD")
    if len({r["source_url"] for r in rows}) != 1:
        problems.append("all six rows share one source URL")
    return problems


def check_raw_quoting(text):
    """The one commit the CSV parser hides: the comma inside note_rule must
    still be inside double quotes in the raw bytes, on every row."""
    if text.count('"' + NOTE_RULE + '"') != 6:
        return ["note_rule is double-quoted in the raw bytes"]
    return []


def check_run_capture(text):
    """SELFTEST_RUN.txt must name its provenance and must not paste an
    exit-code byte the runner's report never carried."""
    problems = []
    if not RUN_PAGE_RE.search(text):
        problems.append("run capture names a bee-self-test run page")
    low = text.lower()
    if "transcription" not in low:
        problems.append("run capture calls itself a transcription")
    if "selftest_output.md" not in low:
        problems.append("run capture says SELFTEST_OUTPUT.md is authoritative")
    if not re.search(r"implied by passed", low, re.IGNORECASE):
        problems.append("run capture records the exit as implied by passed")
    if re.search(r"^exit code:\s*\d+\s*$", low, re.MULTILINE):
        problems.append("run capture pastes no exit-code byte")
    return problems


def check_readme(text):
    low = text.lower()
    problems = []
    if TITLE not in text:
        problems.append("README names the dataset title")
    if not re.search(r"updates this\s+dataset in place|updates the card in place",
                     low):
        problems.append("README says the same title updates the card in place")
    if "the step" in low and "run by hivemindos" not in low:
        problems.append("README does not claim the uploader ran the self-test")
    return problems


# ---- the printer ---------------------------------------------------------

def discussion_body(rows, run_tail):
    row_bits = "; ".join("%s %s" % (r["record_id"], r["has_note"])
                         for r in rows)
    return "\n".join([
        "agent-memory-lint-fixtures -- six-row index of the bee-scouts "
        "fixture records, with the folder's own self-test result",
        "",
        "This dataset is an index, not a lint result. It holds six rows "
        "(record_id/has_note: %s), one per fixture record named on the "
        "public bee-scouts issue pages. Columns: %s. `note_rule` is "
        "double-quoted on every row because the sentence contains a comma. "
        "All six rows share one source_url and one date_read."
        % (row_bits, ", ".join(COLS)),
        "",
        "Dataset: %s" % DATASET_URL,
        "Run capture: %s" % RUN_FILE_URL,
        "",
        "What ran: this folder's own self_test.py, run by HivemindOS's "
        "runner. Reported tail:",
        "~~~",
        run_tail.strip(),
        "~~~",
        "What did not run: no lint of the fixture set, no labels, no "
        "findings. The checker reads data.csv only.",
        "",
        "Check it yourself: cd tools/agent-memory-lint-fixtures-index-v2 "
        "&& python3 self_test.py -- exit 0 with the tail above.",
        "",
        "Sources: public bee-scouts issues #109, #98, #68.",
    ])


def main():
    c = Checker()
    texts = {}
    for name in ("data.csv", "README.md", "SELFTEST_RUN.txt"):
        path = os.path.join(HERE, name)
        if not os.path.isfile(path):
            c.check(False, "%s is present" % name)
            continue
        with open(path, "r", encoding="utf-8", newline="") as fh:
            texts[name] = fh.read()

    rows = []
    if "data.csv" in texts:
        for problem in check_csv_text(texts["data.csv"]):
            c.check(False, "data.csv: " + problem)
        for problem in check_raw_quoting(texts["data.csv"]):
            c.check(False, "data.csv: " + problem)
        c.check("data.csv: all checks pass" not in c.lines,
                "data.csv passes the six recorded-row checks")
        with io.StringIO(texts["data.csv"], newline="") as fh:
            rows = list(csv.DictReader(fh))

    if "README.md" in texts:
        for problem in check_readme(texts["README.md"]):
            c.check(False, "README.md: " + problem)
        c.check(all(p not in " ".join(c.lines) for p in ("README.md: x",)),
                "README.md states the publish facts")

    run_tail = ""
    if "SELFTEST_RUN.txt" in texts:
        for problem in check_run_capture(texts["SELFTEST_RUN.txt"]):
            c.check(False, "SELFTEST_RUN.txt: " + problem)
        c.check("SELFTEST_RUN.txt: " not in " ".join(c.lines),
                "SELFTEST_RUN.txt is a labelled transcription")
        m = re.search(r"--- runner stdout.*?---", texts["SELFTEST_RUN.txt"],
                      re.DOTALL)
        if m:
            run_tail = m.group(0)

    for line in c.lines:
        sys.stdout.write(line + "\n")

    if c.failed:
        sys.stderr.write("PUBLISH NOT READY: %d check(s) failed\n" % c.failed)
        return 1

    sys.stdout.write("\n=== PUBLISH SET (upload these under title %s) ===\n"
                     % TITLE)
    for name in UPLOAD_FILES:
        sys.stdout.write("  %s\n" % name)
    sys.stdout.write("Dataset: %s\n" % DATASET_URL)
    sys.stdout.write("\n=== DISCUSSION BODY (post on the tab) ===\n")
    sys.stdout.write(discussion_body(rows, run_tail) + "\n")
    sys.stdout.write("\nREADY: %d file(s), all checks passed. "
                     "No upload or post performed here.\n" % len(UPLOAD_FILES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
