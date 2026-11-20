#!/usr/bin/env python3
"""Self-test for duckophila-stated-facts. No args, no network.

Runs the tool's own code (build_facts) on its committed sample
data (facts.csv) and compares the result with what is expected.
Exit 0 only when every check passes.
"""

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FACTS = os.path.join(HERE, "facts.csv")


def fail(msg):
    sys.stderr.write("FAIL: %s\n" % msg)
    return 1


def load_tool():
    sys.dont_write_bytecode = True
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    import build_facts
    return build_facts


def main():
    try:
        tool = load_tool()
    except Exception as e:
        return fail("could not import build_facts: %s: %s" % (type(e).__name__, e))

    checks = []

    # 1. The tool's built rows validate cleanly.
    problems = tool.validate(tool.ROWS)
    if problems:
        return fail("built rows do not validate: %s" % problems)
    checks.append("built rows validate: %d rows" % len(tool.ROWS))

    # 2. Every built row has a non-empty http(s) source_url and a
    #    known label, and no duplicate fact.
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

    # 3. Only the two allowed sources appear.
    allowed = {tool.DUCKOPHILA, tool.MICRODUCK}
    used = {r[1] for r in tool.ROWS}
    if not used <= allowed:
        return fail("rows use a source outside the two allowed ones: %s" % (used - allowed))
    if used != allowed:
        return fail("not both allowed sources are used: %s" % (allowed - used))
    checks.append("all rows use only the two allowed sources, and both appear")

    # 4. The committed facts.csv matches the tool's built rows.
    if not os.path.exists(FACTS):
        return fail("facts.csv not found")
    on_disk, errs = tool.read_csv(FACTS)
    if errs:
        return fail("facts.csv: %s" % "; ".join(errs))
    if tool.render(on_disk) != tool.render(tool.ROWS):
        return fail("facts.csv does not match the built rows; rerun build_facts.py")
    if len(on_disk) != len(tool.ROWS):
        return fail("facts.csv has %d rows, expected %d" % (len(on_disk), len(tool.ROWS)))
    checks.append("facts.csv matches the built rows (%d rows)" % len(on_disk))

    # 5. Every committed row has a non-empty source_url too (direct
    #    read of the CSV, independent of the tool's render).
    with open(FACTS, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(tool.FIELDS):
            return fail("facts.csv header %r != %r" % (reader.fieldnames, list(tool.FIELDS)))
        for n, row in enumerate(reader, 2):
            if not (row.get("source_url") or "").strip():
                return fail("facts.csv line %d: empty source_url" % n)
    checks.append("every committed row has a non-empty source_url")

    # 6. The validator rejects the cases it is meant to reject.
    #    The duplicate case must repeat a fact already seen above
    #    (case/whitespace-insensitively), otherwise no duplicate
    #    is detected.
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

    for line in checks:
        print(line)
    print("self-test: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
