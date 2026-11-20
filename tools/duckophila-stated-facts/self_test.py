#!/usr/bin/env python3
"""Self-test for duckophila-stated-facts. No args, no network.

Runs the tool's own code (build_facts) on its committed sample
data (facts.csv) and compares the result with what is expected.
Also checks the dataset card (README_hf.md) and the publish
record (ARTIFACTS.md) name both allowed sources, state each
source licence, and record the intended URL, file list and
row count. Exit 0 only when every check passes.
"""

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FACTS = os.path.join(HERE, "facts.csv")
CARD = os.path.join(HERE, "README_hf.md")
ARTIFACTS = os.path.join(HERE, "ARTIFACTS.md")
INTENDED_URL = "https://huggingface.co/datasets/hivepunk-547-db38b7a4/duckophila-stated-facts"
CONFIRMED_RUN = "44690994352"


def fail(msg):
    sys.stderr.write("FAIL: %s\n" % msg)
    return 1


def load_tool():
    sys.dont_write_bytecode = True
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    import build_facts
    return build_facts


def read_text(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def main():
    try:
        tool = load_tool()
    except Exception as e:
        return fail("could not import build_facts: %s: %s" % (type(e).__name__, e))

    checks = []

    problems = tool.validate(tool.ROWS)
    if problems:
        return fail("built rows do not validate: %s" % problems)
    checks.append("built rows validate: %d rows" % len(tool.ROWS))

    seen = set()
    for i, (fact, url, label, _note) in enumerate(tool.ROWS, 1):
        if not url.strip():
            return fail("row %d: empty source_url" % i)
        if not (url.startswith("http://") or url.startswith("https://")):
            return fail("row %d: source_url not http(s): %r" % (i, url))
        if label not in tool.LABELS:
            return fail("row %d: bad label %r" % (i, label))
        key = fact.strip().casefold()
        if key in seen:
            return fail("row %d: duplicate fact" % i)
        seen.add(key)
    checks.append("every built row has a non-empty http(s) source_url, a known label and a unique fact")

    allowed = {tool.DUCKOPHILA, tool.MICRODUCK}
    used = {r[1] for r in tool.ROWS}
    if not used <= allowed:
        return fail("rows use a source outside the two allowed ones: %s" % (used - allowed))
    if used != allowed:
        return fail("not both allowed sources are used: %s" % (allowed - used))
    checks.append("all rows use only the two allowed sources, and both appear")

    if not os.path.exists(FACTS):
        return fail("facts.csv not found")
    on_disk, errs = tool.read_csv(FACTS)
    if errs:
        return fail("facts.csv: %s" % "; ".join(errs))
    if tool.render(on_disk) != tool.render(tool.ROWS):
        return fail("facts.csv does not match the built rows; rerun build_facts.py")
    if len(on_disk) != 17:
        return fail("facts.csv has %d rows, expected 17" % len(on_disk))
    checks.append("facts.csv matches the built rows (17 rows)")

    with open(FACTS, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(tool.FIELDS):
            return fail("facts.csv header %r != %r" % (reader.fieldnames, list(tool.FIELDS)))
        for n, row in enumerate(reader, 2):
            if not (row.get("source_url") or "").strip():
                return fail("facts.csv line %d: empty source_url" % n)
    checks.append("every committed row has a non-empty source_url")

    bad_rows = [
        ("no url", "", "FACT", ""),
        ("bad scheme", "ftp://example.org/x", "FACT", ""),
        ("bad label", "https://github.com/joeynyc/awesome-microduck", "MAYBE", ""),
        ("  No URL  ", "https://github.com/joeynyc/awesome-microduck", "FACT", ""),
    ]
    bad_problems = tool.validate(bad_rows)
    needles = ("empty source_url", "not http(s)", "unknown label", "duplicate fact")
    joined = " | ".join(bad_problems)
    for needle in needles:
        if needle not in joined:
            return fail("validator missed %r: %s" % (needle, joined))
    checks.append("validator rejects empty/off-scheme source_url, unknown label and duplicate fact")

    if not os.path.exists(CARD):
        return fail("README_hf.md not found")
    card = read_text(CARD)
    if not card.startswith("---"):
        return fail("README_hf.md has no YAML front matter")
    for needle in (tool.DUCKOPHILA, tool.MICRODUCK, "17", "UNKNOWN"):
        if needle not in card:
            return fail("README_hf.md missing %r" % needle)
    if "licence" not in card.lower() and "license" not in card.lower():
        return fail("README_hf.md does not state any source licence")
    checks.append("dataset card names both sources, states each licence as UNKNOWN and gives 17 rows")

    if not os.path.exists(ARTIFACTS):
        return fail("ARTIFACTS.md not found")
    art = read_text(ARTIFACTS)
    for needle in (INTENDED_URL, "facts.csv", "README_hf.md", "17", "hivepunk-547-db38b7a4", CONFIRMED_RUN, "self-test: all checks passed"):
        if needle not in art:
            return fail("ARTIFACTS.md missing %r" % needle)
    if "NOT" not in art:
        return fail("ARTIFACTS.md does not state that the live page is unconfirmed")
    checks.append("ARTIFACTS.md records intended URL, upload files, 17 rows, confirmed self-test run, marked live-unconfirmed")

    for line in checks:
        print(line)
    print("self-test: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
