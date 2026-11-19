#!/usr/bin/env python3
"""Self-test for stated-facts-check. No args, no network."""

import contextlib
import io
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HEADER = "fact_id,topic,claim,source\n"


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
        return __import__("stated_facts_check")
    except Exception as e:
        raise Fail("could not import stated_facts_check: %s: %s" % (type(e).__name__, e))


def write(root, name, text):
    path = os.path.join(root, name)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return path


def run_main(mod, argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = mod.main(argv)
    return code, buf.getvalue()


def main():
    try:
        mod = import_tool()
        checks = []
        with tempfile.TemporaryDirectory() as tmp:
            good = write(tmp, "good.csv", HEADER + "1,about,DuckSpace example fact one.,https://duckspace.org/about\n2,features,\"Fact, with comma.\",https://www.duckspace.org/features\n\n3,contact,Contact page exists.,https://sub.duckspace.org/contact\n")
            report, problems, skipped = mod.check_file(good, ["duckspace.org"])
            check(not problems, "good: %r" % (problems,))
            check(report["total"] == 3 and report["valid"] == 3, "good counts: %r" % (report,))
            check(skipped == 1, "blank skipped: %r" % (skipped,))
            checks.append("valid rows incl. quoted comma and subdomains pass; blank row skipped")

            dup = write(tmp, "dup.csv", HEADER + "1,a,Same claim.,https://duckspace.org/a\n1,b,Same claim.,https://duckspace.org/b\n")
            report, problems, _ = mod.check_file(dup)
            check(any("duplicate fact_id" in p for p in problems), "dup id: %r" % (problems,))
            check(any("duplicate claim" in p for p in problems), "dup claim: %r" % (problems,))
            checks.append("duplicate fact_id and duplicate claim reported")

            badsrc = write(tmp, "bad.csv", HEADER + "1,a,Fact one.,duckspace.org/a\n2,b,Fact two.,ftp://duckspace.org/b\n3,c,Fact three.,https://evil.example/c\n")
            report, problems, _ = mod.check_file(badsrc, ["duckspace.org"])
            check(sum("not a valid" in p for p in problems) == 2, "bad urls: %r" % (problems,))
            check(any("not in allowed" in p for p in problems), "domain: %r" % (problems,))
            checks.append("schemeless, wrong-scheme and off-domain sources flagged")

            empty = write(tmp, "empty.csv", HEADER + "1,, ,https://duckspace.org/a\n")
            report, problems, _ = mod.check_file(empty)
            check(any("empty topic" in p for p in problems) and any("empty claim" in p for p in problems), "empty: %r" % (problems,))
            checks.append("empty topic/claim flagged")

            missing_col = write(tmp, "col.csv", "fact_id,topic,claim\n1,a,Fact.,\n")
            report, problems, _ = mod.check_file(missing_col)
            check(any("missing column" in p for p in problems), "col: %r" % (problems,))
            extra_col = write(tmp, "extra.csv", HEADER.rstrip() + ",note\n1,a,Fact.,https://duckspace.org/a,hi\n")
            report, problems, _ = mod.check_file(extra_col)
            check(any("unexpected column" in p for p in problems), "extra col: %r" % (problems,))
            checks.append("missing and unexpected columns flagged")

            report, problems, _ = mod.check_file(os.path.join(tmp, "nope.csv"))
            check(report is None and any("not found" in p for p in problems), "missing: %r" % (problems,))
            blank = write(tmp, "blank.csv", "")
            report, problems, _ = mod.check_file(blank)
            check(report is not None and any("header" in p for p in problems), "blank: %r" % (problems,))
            checks.append("missing file and empty file fail clearly")

            code, out = run_main(mod, ["stated_facts_check.py", good, "--allow-domain", "duckspace.org"])
            check(code == 0 and "PASS:" in out and "counts:" in out, "CLI good: %r %r" % (code, out))
            code, out = run_main(mod, ["stated_facts_check.py", dup])
            check(code == 1 and "FAIL:" in out, "CLI dup: %r %r" % (code, out))
            code, out = run_main(mod, ["stated_facts_check.py"])
            check(code == 2 and "usage" in out, "CLI usage: %r %r" % (code, out))
            out_path = os.path.join(tmp, "report.txt")
            code, out = run_main(mod, ["stated_facts_check.py", good, "-o", out_path])
            check(code == 0 and os.path.exists(out_path), "CLI -o: %r %r" % (code, out))
            with open(out_path, encoding="utf-8") as fh:
                check("PASS:" in fh.read(), "report file contents")
            checks.append("CLI exits 0 PASS, 1 FAIL, 2 usage; -o writes report")

            rows = [{"fact_id": "1", "topic": "a", "claim": "Fact.", "source": "https://duckspace.org/a", "_line": 2}]
            valid, problems = mod.check_rows(rows, ["duckspace.org"])
            check(valid == 1 and not problems, "check_rows: %r %r" % (valid, problems))
            check(mod.is_http_url("https://duckspace.org/x") and not mod.is_http_url("duckspace.org/x"), "is_http_url")
            checks.append("check_rows() and is_http_url() behave as documented")
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
