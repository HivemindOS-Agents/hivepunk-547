#!/usr/bin/env python3
"""Self-test for card-files-sync.

Run from this folder with no arguments and no network. Imports
sync_check, checks the included README.md + data.csv match, then
checks synthetic fixtures in a temp directory: a matching pair, a
mismatch (missing + extra), duplicates on each side, quoted names
including a quoted name containing a comma, a missing Files section,
and missing files. Also checks CLI exit codes 0/1. Exits 0 only if
all checks pass.
"""

import contextlib
import io
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ["sync_check.py", "README.md", "self_test.py", "data.csv"]


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
        return __import__("sync_check")
    except Exception as e:
        raise Fail("could not import sync_check: %s: %s" % (type(e).__name__, e))


def write(folder, name, text):
    path = os.path.join(folder, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def csv_text(names):
    lines = ["file_name,description"]
    for n in names:
        if "," in n:
            lines.append('"%s",Quoted name with comma' % n)
        else:
            lines.append("%s,desc for %s" % (n, n))
    return "\n".join(lines) + "\n"


def card_text(files, heading="## Files"):
    parts = ["# sample-dataset\n\n%s\n\n" % heading]
    parts.extend("- %s\n" % f for f in files)
    parts.append("\n## Notes\n\nDone.\n")
    return "".join(parts)


def main():
    try:
        mod = import_tool()
        checks = []

        ok, problems, listed, csv_names = mod.verify(
            os.path.join(HERE, "README.md"), os.path.join(HERE, "data.csv"))
        check(ok, "included card + data.csv failed: %r" % (problems,))
        check(csv_names == FILES, "included csv names are %r" % (csv_names,))
        check(sorted(listed) == sorted(FILES), "included list is %r" % (listed,))
        checks.append("included README.md + data.csv match: %s" % ", ".join(FILES))

        with tempfile.TemporaryDirectory() as tmp:
            good_csv = write(tmp, "data.csv", csv_text(["alpha.py", "beta.py"]))
            good_md = write(tmp, "README.md", card_text(["alpha.py", "beta.py"]))
            ok, problems, _, _ = mod.verify(good_md, good_csv)
            check(ok, "matching fixture failed: %r" % (problems,))
            checks.append("matching fixture passes")

            alt_heading = write(tmp, "alt.md", card_text(["alpha.py", "beta.py"], heading="## File list"))
            ok, problems, _, _ = mod.verify(alt_heading, good_csv)
            check(ok, "## File list heading failed: %r" % (problems,))
            checks.append("'## File list' heading also accepted")

            quoted_csv = write(tmp, "quoted.csv", csv_text(["quoted.py", "data,set.csv", "plain.py"]))
            quoted_md = write(tmp, "quoted.md", card_text(["quoted.py", "data,set.csv", "plain.py"]))
            ok, problems, listed, csv_names = mod.verify(quoted_md, quoted_csv)
            check(ok, "quoted-name fixture failed: %r" % (problems,))
            check(csv_names == ["quoted.py", "data,set.csv", "plain.py"], "quoted csv names %r" % (csv_names,))
            check(listed == csv_names, "quoted listed %r" % (listed,))
            checks.append("quoted names (incl. comma) match on both sides")

            mism_csv = write(tmp, "mism.csv", csv_text(["alpha.py", "beta.py", "gamma.py"]))
            mism_md = write(tmp, "mism.md", card_text(["alpha.py", "stray.py"]))
            ok, problems, _, _ = mod.verify(mism_md, mism_csv)
            check(not ok, "mismatch fixture unexpectedly passed")
            joined = " ".join(problems)
            check("missing from card: beta.py, gamma.py" in joined, "missing not listed: %r" % (problems,))
            check("extra names not in data.csv: stray.py" in joined, "extra not listed: %r" % (problems,))
            checks.append("mismatch lists missing (beta.py, gamma.py) and extra (stray.py)")

            dup_csv = write(tmp, "dup.csv", csv_text(["alpha.py", "alpha.py", "beta.py"]))
            ok, problems, _, _ = mod.verify(good_md, dup_csv)
            check(not ok and any("data.csv duplicate(s): alpha.py" in p for p in problems), "csv duplicate: %r" % (problems,))
            checks.append("duplicate in data.csv fails and names alpha.py")

            dup_md = write(tmp, "dup.md", card_text(["alpha.py", "beta.py", "beta.py"]))
            ok, problems, _, _ = mod.verify(dup_md, good_csv)
            check(not ok and any("file list duplicate(s): beta.py" in p for p in problems), "list duplicate: %r" % (problems,))
            checks.append("duplicate in Files list fails and names beta.py")

            no_section = write(tmp, "none.md", "# sample\n\nNo list here.\n")
            ok, problems, _, _ = mod.verify(no_section, good_csv)
            check(not ok and any("Files" in p for p in problems), "no section: %r" % (problems,))
            checks.append("missing Files section fails and mentions 'Files'")

            ok, problems, _, _ = mod.verify(os.path.join(tmp, "missing.md"), good_csv)
            check(not ok and any("not found" in p for p in problems), "missing readme: %r" % (problems,))
            ok, problems, _, _ = mod.verify(good_md, os.path.join(tmp, "missing.csv"))
            check(not ok and any("not found" in p for p in problems), "missing csv: %r" % (problems,))
            checks.append("missing README and missing data.csv fail with 'not found'")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["sync_check.py", good_md, good_csv])
            check(code == 0 and buf.getvalue().startswith("ok:"), "CLI good %r %r" % (code, buf.getvalue()))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["sync_check.py", mism_md, mism_csv])
            check(code == 1 and "FAIL:" in buf.getvalue(), "CLI bad %r %r" % (code, buf.getvalue()))
            checks.append("CLI exits 0 with ok for match and 1 with FAIL for mismatch")
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
