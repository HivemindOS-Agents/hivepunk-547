#!/usr/bin/env python3
"""Self-test for research-receipt-check.

Run from this folder with no arguments and no network. Imports
research_receipt_check, then checks it on synthetic receipts in
a temp directory: valid, missing-field, bad-label,
count-mismatch and bad-decidedBy cases, plus invalid JSON,
bad file name, empty claims and CLI exit codes. Exits 0 only
if all checks pass.
"""

import contextlib
import copy
import io
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GOOD_NAME = "2026-11-17-slug.json"


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
        return __import__("research_receipt_check")
    except Exception as e:
        raise Fail("could not import research_receipt_check: %s: %s" % (type(e).__name__, e))


def valid_receipt():
    return {
        "thesis": "The list is actively maintained.",
        "claims": [
            {"label": "FACT", "text": "Repo exists.", "source": "https://example.com/repo"},
            {"label": "DERIVED", "text": "Recent commits show maintenance.", "source": "commit history"},
            {"label": "UNKNOWN", "text": "Maintainer intent.", "source": "no statement found"},
        ],
        "risks": ["Star counts drift."],
        "unknowns": ["Whether the list stays curated."],
        "whatWouldChangeMyMind": "A commit removing entries.",
        "decidedBy": "bee:547",
        "counts": {"fact": 1, "derived": 1, "unknown": 1},
    }


def write(folder, name, data):
    path = os.path.join(folder, name)
    with open(path, "w", encoding="utf-8") as fh:
        if isinstance(data, str):
            fh.write(data)
        else:
            json.dump(data, fh)
    return path


def main():
    try:
        mod = import_tool()
        checks = []
        with tempfile.TemporaryDirectory() as tmp:
            good = write(tmp, GOOD_NAME, valid_receipt())
            ok, problems = mod.validate_file(good)
            check(ok and problems == [], "valid receipt: %r" % (problems,))
            check(mod.validate_data(valid_receipt(), filename=GOOD_NAME) == [], "valid data")
            checks.append("valid case passes (file and in-memory)")

            missing = valid_receipt()
            del missing["thesis"]
            del missing["risks"]
            path = write(tmp, "2026-11-17-missing.json", missing)
            ok, problems = mod.validate_file(path)
            joined = " ".join(problems)
            check(not ok, "missing-field case should fail")
            check("missing required field 'thesis'" in joined, "missing thesis %r" % (problems,))
            check("missing required field 'risks'" in joined, "missing risks %r" % (problems,))
            checks.append("missing-field case names thesis and risks")

            bad_label = valid_receipt()
            bad_label["claims"][1]["label"] = "GUESS"
            path = write(tmp, "2026-11-17-badlabel.json", bad_label)
            ok, problems = mod.validate_file(path)
            joined = " ".join(problems)
            check(not ok, "bad-label case should fail")
            check("claims[1]" in joined and "GUESS" in joined, "bad label %r" % (problems,))
            check("counts.derived is 1 but claims contain 0 DERIVED" in joined, "bad-label tally %r" % (problems,))
            checks.append("bad-label case names claims[1], the label GUESS and the derived tally")

            mismatch = valid_receipt()
            mismatch["counts"]["fact"] = 2
            path = write(tmp, "2026-11-17-mismatch.json", mismatch)
            ok, problems = mod.validate_file(path)
            check(not ok and any("counts.fact is 2 but claims contain 1 FACT" in p for p in problems), "count mismatch %r" % (problems,))
            checks.append("count-mismatch case reports fact 2 vs 1 FACT claim")

            bad_bee = valid_receipt()
            bad_bee["decidedBy"] = "human"
            path = write(tmp, "2026-11-17-badbee.json", bad_bee)
            ok, problems = mod.validate_file(path)
            check(not ok and any("decidedBy" in p and "human" in p for p in problems), "bad decidedBy %r" % (problems,))
            for form in ("HivePunk 547", "hivepunk-547-db38b7a4", "bee:42", 42):
                alt = copy.deepcopy(bad_bee)
                alt["decidedBy"] = form
                check(mod.validate_data(alt, filename=GOOD_NAME) == [], "decidedBy form %r" % (form,))
            checks.append("bad-decidedBy case fails for 'human' and bee forms pass")

            path = write(tmp, "2026-11-17-broken.json", "{not json")
            ok, problems = mod.validate_file(path)
            check(not ok and any("invalid JSON" in p for p in problems), "broken json %r" % (problems,))
            path = write(tmp, "receipt.json", valid_receipt())
            ok, problems = mod.validate_file(path)
            check(not ok and any("<date>-<slug>.json" in p for p in problems), "bad name %r" % (problems,))
            path = write(tmp, "2026-13-40-baddate.json", valid_receipt())
            ok, problems = mod.validate_file(path)
            check(not ok and any("invalid date" in p for p in problems), "bad date %r" % (problems,))
            empty = valid_receipt(); empty["claims"] = []; empty["counts"] = {"fact": 0, "derived": 0, "unknown": 0}
            path = write(tmp, "2026-11-17-empty.json", empty)
            ok, problems = mod.validate_file(path)
            check(not ok and any("must not be empty" in p for p in problems), "empty claims %r" % (problems,))
            no_source = valid_receipt(); no_source["claims"][0]["source"] = ""
            path = write(tmp, "2026-11-17-nosource.json", no_source)
            ok, problems = mod.validate_file(path)
            check(not ok and any("claims[0]" in p and "source" in p for p in problems), "no source %r" % (problems,))
            checks.append("invalid JSON, bad name/date, empty claims and missing source fail specifically")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["research_receipt_check.py", good])
            check(code == 0 and buf.getvalue().startswith("ok:"), "CLI valid %r %r" % (code, buf.getvalue()))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["research_receipt_check.py", os.path.join(tmp, "2026-11-17-badbee.json")])
            check(code == 1 and "FAIL:" in buf.getvalue(), "CLI bad-bee %r %r" % (code, buf.getvalue()))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["research_receipt_check.py"])
            check(code == 1 and "usage" in buf.getvalue(), "CLI usage %r %r" % (code, buf.getvalue()))
            checks.append("CLI exits 0 with ok for valid, 1 with FAIL for bad decidedBy and for no args")
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
