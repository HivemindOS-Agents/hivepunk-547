#!/usr/bin/env python3
"""Self-test for artifacts-link-check.

Run from this folder with no arguments and no network. Imports
artifacts_link_check and checks it on synthetic temp fixtures:
valid Markdown + bare links, duplicates, empty targets,
malformed targets, code-block ignoring, missing/empty input,
and CLI exit codes. Exits 0 only if all checks pass.
"""

import contextlib
import io
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FENCE = "`" * 3


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
        return __import__("artifacts_link_check")
    except Exception as e:
        raise Fail("could not import artifacts_link_check: %s: %s" % (type(e).__name__, e))


def write(root, name, text):
    path = os.path.join(root, name)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return path


def main():
    try:
        mod = import_tool()
        checks = []
        with tempfile.TemporaryDirectory() as tmp:
            good = write(tmp, "ARTIFACTS.md", "\n".join([
                "# Artifacts", "",
                "- [Dataset](https://huggingface.co/datasets/example/data)",
                "- Bare: https://example.org/page.",
                "- Relative: [guide](docs/guide.md) and [anchor](#top)",
                "- Mail: [mail](mailto:a@example.org)",
                FENCE, "https://ignored.example/in-code", FENCE, ""]))
            report, problems = mod.check_file(good)
            check(not problems, "good: %r" % (problems,))
            check(report["total"] == 5 and report["markdown"] == 4 and report["bare"] == 1,
                  "good counts: %r" % (report,))
            check(report["valid"] == 5, "good valid: %r" % (report["valid"],))
            checks.append("valid Markdown, bare, relative, anchor and mailto links pass; code fence ignored")

            dup = write(tmp, "dup.md", "[a](https://example.org/x)\n[b](https://example.org/x)\n")
            report, problems = mod.check_file(dup)
            check(report["duplicates"] == 1 and any("duplicate" in p for p in problems), "dup: %r %r" % (report, problems))
            checks.append("duplicate URL reported with count")

            empty = write(tmp, "empty.md", "[nothing]()\n")
            report, problems = mod.check_file(empty)
            check(report["empty"] == 1 and any("empty" in p for p in problems), "empty: %r %r" % (report, problems))
            checks.append("empty link target reported")

            bad = write(tmp, "bad.md", "[x](https://exa mple.org)\n[y](example.com/page)\n[z](https://example.org/unclosed\n")
            report, problems = mod.check_file(bad)
            check(report["malformed"] >= 2, "bad: %r %r" % (report, problems))
            checks.append("whitespace, schemeless domain and broken Markdown flagged malformed")

            report, problems = mod.check_file(os.path.join(tmp, "missing.md"))
            check(report is None and any("not found" in p for p in problems), "missing: %r" % (problems,))
            blank = write(tmp, "blank.md", "   \n")
            report, problems = mod.check_file(blank)
            check(report is None and any("empty" in p for p in problems), "blank: %r" % (problems,))
            nolinks = write(tmp, "nolinks.md", "just text, no links\n")
            report, problems = mod.check_file(nolinks)
            check(report is not None and any("no links" in p for p in problems), "nolinks: %r" % (problems,))
            checks.append("missing, empty and link-free input fail clearly")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["artifacts_link_check.py", good])
            check(code == 0 and "PASS:" in buf.getvalue() and "counts:" in buf.getvalue(), "CLI good: %r %r" % (code, buf.getvalue()))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["artifacts_link_check.py", dup])
            check(code == 1 and "FAIL:" in buf.getvalue(), "CLI dup: %r %r" % (code, buf.getvalue()))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["artifacts_link_check.py", os.path.join(tmp, "nope.md")])
            check(code == 1 and "FAIL:" in buf.getvalue(), "CLI missing: %r %r" % (code, buf.getvalue()))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["artifacts_link_check.py"])
            check(code == 2 and "usage" in buf.getvalue(), "CLI usage: %r %r" % (code, buf.getvalue()))
            checks.append("CLI exits 0 on PASS, 1 on problems/missing, 2 on usage error")

            links = mod.extract_links("[a](https://example.org/) https://example.net/\n")
            check(len(links) == 2 and links[0]["kind"] == "markdown" and links[1]["kind"] == "bare", "extract: %r" % (links,))
            checks.append("extract_links() returns Markdown and bare links with kinds")
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
