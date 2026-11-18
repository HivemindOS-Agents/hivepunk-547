#!/usr/bin/env python3
"""Self-test for artifacts-index-check.

Run from this folder with no arguments and no network. Imports
artifacts_index_check, then checks it on synthetic ARTIFACTS.md
files in a temp directory: valid, missing-file, malformed-URL
and empty-index cases, plus a missing index file and CLI exit
codes. Exits 0 only if all checks pass.
"""

import contextlib
import io
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


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
        return __import__("artifacts_index_check")
    except Exception as e:
        raise Fail("could not import artifacts_index_check: %s: %s" % (type(e).__name__, e))


def write(folder, rel, text):
    path = os.path.join(folder, rel)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


VALID = """# Artifacts

- Report | `notes/report.md` | https://example.org/report
- Data | [data](data/items.csv) | https://example.org/data

| Tool | `tools/check.py` | https://example.org/tool |
"""


def main():
    try:
        mod = import_tool()
        checks = []
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, "notes/report.md", "report\n")
            write(tmp, "data/items.csv", "a,b\n")
            write(tmp, "tools/check.py", "# ok\n")
            good = write(tmp, "ARTIFACTS.md", VALID)
            ok, problems, stats = mod.check_file(good)
            check(ok and problems == [], "valid index: %r" % (problems,))
            check("3 entries" in stats and "3 local file(s)" in stats and "3 URL(s)" in stats, "valid stats %r" % stats)
            entries = mod.parse_entries(VALID)
            check(len(entries) == 3, "parsed %d entries" % len(entries))
            checks.append("valid case passes (3 entries, 3 files, 3 URLs)")

            missing = write(tmp, "missing/ARTIFACTS.md", VALID)
            write(tmp, "missing/notes/report.md", "r\n")
            ok, problems, _ = mod.check_file(missing)
            joined = " ".join(problems)
            check(not ok, "missing-file case should fail")
            check("listed local file not found: data/items.csv" in joined, "missing csv %r" % (problems,))
            check("listed local file not found: tools/check.py" in joined, "missing py %r" % (problems,))
            check("line 4" in joined and "line 6" in joined or "line 7" in joined, "line numbers %r" % (problems,))
            checks.append("missing-file case names data/items.csv and tools/check.py")

            bad_url_text = "# Artifacts\n\n- Broken | `notes/report.md` | https://\n- NoHost | `notes/report.md` | http://nodot\n- BadScheme | `notes/report.md` | ftp://example.org/x\n"
            bad = write(tmp, "badurl/ARTIFACTS.md", bad_url_text)
            write(tmp, "badurl/notes/report.md", "r\n")
            ok, problems, _ = mod.check_file(bad)
            joined = " ".join(problems)
            check(not ok, "malformed-URL case should fail")
            check("malformed URL" in joined, "malformed mention %r" % (problems,))
            check(mod.url_problem("https://example.org/x") is None, "good url")
            check(mod.url_problem("https://") is not None, "empty host")
            check(mod.url_problem("http://nodot") is not None, "undotted host")
            check(mod.url_problem("ftp://example.org/x") is not None, "bad scheme")
            check(mod.url_problem("https://example.org:99999/x") is not None, "bad port")
            check(mod.url_problem("https://exam ple.org/x") is not None, "space in url")
            checks.append("malformed-URL case fails and url_problem flags host/scheme/port/space")

            empty = write(tmp, "empty/ARTIFACTS.md", "# Artifacts\n\nNo entries yet.\n")
            ok, problems, _ = mod.check_file(empty)
            check(not ok and any("no artifact entries found" in p for p in problems), "empty index %r" % (problems,))
            blank = write(tmp, "blank/ARTIFACTS.md", "")
            ok, problems, _ = mod.check_file(blank)
            check(not ok and any("no artifact entries found" in p for p in problems), "blank index %r" % (problems,))
            checks.append("empty-index case reports no artifact entries found")

            ok, problems, _ = mod.check_file(os.path.join(tmp, "nope", "ARTIFACTS.md"))
            check(not ok and any("not found" in p for p in problems), "missing index %r" % (problems,))
            checks.append("missing index file fails with not found")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["artifacts_index_check.py", good])
            check(code == 0 and buf.getvalue().startswith("ok:"), "CLI valid %r %r" % (code, buf.getvalue()))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["artifacts_index_check.py", missing])
            check(code == 1 and "FAIL:" in buf.getvalue() and "not found" in buf.getvalue(), "CLI missing %r %r" % (code, buf.getvalue()))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["artifacts_index_check.py", empty])
            check(code == 1 and "no artifact entries" in buf.getvalue(), "CLI empty %r %r" % (code, buf.getvalue()))
            checks.append("CLI exits 0 with ok for valid, 1 with FAIL for missing-file and empty")
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
