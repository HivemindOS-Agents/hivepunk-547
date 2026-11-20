#!/usr/bin/env python3
"""Self-test for microduck-stated-facts. No args, no network.

Runs the tool's own code (build_facts) on its committed sample
data (facts.csv) and compares the result with what is expected,
including the row count in MANIFEST.json. Also checks the dataset
card names the sources, gives the row count and marks unverified
licences UNKNOWN. Exit 0 only when every check passes.
"""

import contextlib
import io
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FACTS = os.path.join(HERE, "facts.csv")
MANIFEST = os.path.join(HERE, "MANIFEST.json")
CARD = os.path.join(HERE, "README_hf.md")
EXPECTED_ROWS = 24


class Fail(Exception):
    pass


def check(cond, msg):
    if not cond:
        raise Fail(msg)


def import_tool():
    sys.dont_write_bytecode = True
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    try:
        return __import__("build_facts")
    except Exception as e:
        raise Fail("could not import build_facts: %s: %s" % (type(e).__name__, e))


def run_main(mod, argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = mod.main(argv)
    return code, buf.getvalue()


def main():
    try:
        mod = import_tool()
        checks = []
        rows = mod.rows_with_date()

        problems = mod.validate(rows)
        check(problems == [], "built rows do not validate: %r" % (problems,))
        check(len(rows) == EXPECTED_ROWS, "built rows %d != %d" % (len(rows), EXPECTED_ROWS))
        checks.append("built rows validate (%d rows)" % len(rows))

        for i, (fid, subject, claim, label, url, date) in enumerate(rows, 1):
            check(url.startswith("https://"), "row %d: source_url not https: %r" % (i, url))
            check(url in mod.ALLOWED, "row %d: source outside allowed set: %r" % (i, url))
            check(label in mod.LABELS, "row %d: bad label %r" % (i, label))
            check(date == "2026-11-20", "row %d: observed_date %r" % (i, date))
            check(subject in (mod.MD_SUBJECT, mod.RL_SUBJECT), "row %d: bad subject %r" % (i, subject))
            check(claim.strip(), "row %d: empty claim" % i)
        checks.append("every row uses an allowed https source, a known label, a known subject and the observed date")

        used = {r[4] for r in rows}
        check(mod.REPO in used and mod.REPO_RL in used, "both repo sources must appear")
        labels_used = {r[3] for r in rows}
        check(labels_used == set(mod.LABELS), "all three labels must appear: %r" % (labels_used,))
        checks.append("both repositories are covered and FACT, DERIVED and UNKNOWN all appear")

        bad_rows = [
            ("", "s", "c", "FACT", mod.REPO, "2026-11-20"),
            ("X1", "s", "c", "FACT", "", "2026-11-20"),
            ("X1", "s", "c", "FACT", "ftp://example.org/x", "2026-11-20"),
            ("X1", "s", "c", "MAYBE", mod.REPO, "2026-11-20"),
            ("X1", "s", "c", "FACT", mod.REPO, "20-11-2026"),
            ("X1", "  ", "c", "FACT", mod.REPO, "2026-11-20"),
            ("dup", "s", "c", "FACT", mod.REPO, "2026-11-20"),
            ("dup", "s", "c", "FACT", mod.REPO, "2026-11-20"),
        ]
        joined = " | ".join(mod.validate(bad_rows))
        for needle in ("empty fact_id", "empty source_url", "not http(s)", "unknown label",
                       "observed_date not YYYY-MM-DD", "empty subject", "duplicate fact_id"):
            check(needle in joined, "validator missed %r: %s" % (needle, joined))
        checks.append("validator rejects empty id/url/subject, off-scheme url, unknown label, bad date and duplicate id")

        check(os.path.exists(FACTS), "facts.csv not found")
        on_disk, errs = mod.read_csv(FACTS)
        check(errs == [], "facts.csv: %r" % (errs,))
        check(mod.render(on_disk) == mod.render(rows), "facts.csv does not match the built rows; rerun build_facts.py")
        check(len(on_disk) == EXPECTED_ROWS, "facts.csv has %d rows, expected %d" % (len(on_disk), EXPECTED_ROWS))
        checks.append("facts.csv matches the built rows (%d rows)" % EXPECTED_ROWS)

        check(os.path.exists(MANIFEST), "MANIFEST.json not found")
        with open(MANIFEST, encoding="utf-8") as fh:
            manifest = json.load(fh)
        check(manifest.get("row_count") == EXPECTED_ROWS,
              "manifest row_count %r != %d" % (manifest.get("row_count"), EXPECTED_ROWS))
        check(manifest == mod.manifest_for(rows), "manifest does not match the built rows")
        counts = {}
        for r in on_disk:
            counts[r[3]] = counts.get(r[3], 0) + 1
        check(manifest.get("label_counts") == counts, "manifest label counts %r != %r" % (manifest.get("label_counts"), counts))
        checks.append("MANIFEST.json row_count %d matches facts.csv and its label counts" % EXPECTED_ROWS)

        check(os.path.exists(CARD), "README_hf.md not found")
        with open(CARD, encoding="utf-8") as fh:
            card = fh.read()
        check(card.startswith("---"), "README_hf.md has no YAML front matter")
        for needle in ("microduck-stated-facts", str(EXPECTED_ROWS), "UNKNOWN", "license",
                       "pollen-robotics/microduck", "microduck_rl", "fact_id"):
            check(needle in card, "README_hf.md missing %r" % needle)
        checks.append("dataset card gives the name, row count, columns and marks unverified licences UNKNOWN")

        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "facts.csv")
            man = os.path.join(tmp, "MANIFEST.json")
            code, text = run_main(mod, ["build_facts.py", "-o", out, "-m", man])
            check(code == 0, "CLI write exit %r: %r" % (code, text))
            written, errs = mod.read_csv(out)
            check(errs == [] and mod.render(written) == mod.render(rows), "CLI write mismatch")
            code, text = run_main(mod, ["build_facts.py", "-o", out, "-m", man, "--check"])
            check(code == 0 and "PASS:" in text, "CLI check exit %r: %r" % (code, text))
            with open(out, "a", encoding="utf-8") as fh:
                fh.write("EXTRA,s,c,FACT,%s,2026-11-20\n" % mod.REPO)
            code, text = run_main(mod, ["build_facts.py", "-o", out, "-m", man, "--check"])
            check(code == 1 and "FAIL:" in text, "CLI check should fail on extra row: %r %r" % (code, text))
            code, text = run_main(mod, ["build_facts.py", "--bogus"])
            check(code == 2, "CLI unknown argument exit %r" % (code,))
        checks.append("CLI writes rows, --check passes on a clean copy and fails on a changed one")
    except Fail as e:
        sys.stderr.write("FAIL: %s\n" % e)
        return 1
    except Exception as e:
        sys.stderr.write("FAIL: unexpected %s: %s\n" % (type(e).__name__, e))
        return 1
    for line in checks:
        print(line)
    print("self-test: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
