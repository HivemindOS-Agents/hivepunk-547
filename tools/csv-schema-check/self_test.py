#!/usr/bin/env python3
"""Self-test for csv-schema-check.

Run from this folder with no arguments and no network. Imports
csv_schema_check, then checks it on synthetic CSV fixtures in a
temp directory: valid, missing-column, empty-required, bad-source,
missing-source (empty), header-only and missing-file cases, plus
CLI exit codes. Exits 0 only if all checks pass.
"""

import contextlib
import csv
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
        return __import__("csv_schema_check")
    except Exception as e:
        raise Fail("could not import csv_schema_check: %s: %s" % (type(e).__name__, e))


def write_csv(folder, name, header, rows):
    path = os.path.join(folder, name)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        writer.writerows(rows)
    return path


HEADER = ["tool_name", "description", "detail", "source"]


def main():
    try:
        mod = import_tool()
        checks = []
        with tempfile.TemporaryDirectory() as tmp:
            good = write_csv(tmp, "good.csv", HEADER, [
                ["Letta", "Stateful agents", "Apache-2.0", "https://github.com/letta-ai/letta"],
                ["Mem0", "Memory layer", "Drop-in memory", "https://github.com/mem0ai/mem0"],
            ])
            ok, problems, row_count, notes = mod.check_file(good)
            check(ok and problems == [] and row_count == 2, "valid: %r rows=%r" % (problems, row_count))
            checks.append("valid case passes with 2 rows")

            extra = write_csv(tmp, "extra.csv", HEADER + ["extra_col"], [["A", "d", "x", "https://example.org/a", "e"]])
            ok, problems, row_count, notes = mod.check_file(extra)
            check(ok and any("extra_col" in n for n in notes), "extra: %r %r" % (problems, notes))
            checks.append("extra column allowed and noted")

            missing_col = write_csv(tmp, "missing_col.csv", ["tool_name", "description", "source"], [["A", "d", "https://example.org/a"]])
            ok, problems, row_count, _ = mod.check_file(missing_col)
            joined = " ".join(problems)
            check(not ok and "missing expected column 'detail'" in joined, "missing col: %r" % (problems,))
            checks.append("missing-column case names detail")

            empty_field = write_csv(tmp, "empty.csv", HEADER, [["A", "", "x", "https://example.org/a"], ["B", "d", "y", "https://example.org/b"]])
            ok, problems, row_count, _ = mod.check_file(empty_field)
            joined = " ".join(problems)
            check(not ok and "row 1" in joined and "required field 'description' is empty" in joined, "empty field: %r" % (problems,))
            checks.append("empty-required case names row 1 and description")

            bad_source = write_csv(tmp, "badsrc.csv", HEADER, [["A", "d", "x", "not a url"], ["B", "d", "y", "ftp://example.org/b"], ["C", "d", "z", "https://"]])
            ok, problems, row_count, _ = mod.check_file(bad_source)
            joined = " ".join(problems)
            check(not ok and joined.count("source URL") == 3, "bad source: %r" % (problems,))
            check(mod._is_url("https://example.org/x") and not mod._is_url("not a url") and not mod._is_url("https://"), "url helper")
            checks.append("bad-source case flags all 3 malformed source URLs")

            empty_source = write_csv(tmp, "emptysrc.csv", HEADER, [["A", "d", "x", ""]])
            ok, problems, row_count, _ = mod.check_file(empty_source)
            check(not ok and any("required field 'source' is empty" in p for p in problems), "empty source: %r" % (problems,))
            checks.append("empty source case fails as empty required field")

            header_only = write_csv(tmp, "header_only.csv", HEADER, [])
            ok, problems, row_count, _ = mod.check_file(header_only)
            check(not ok and row_count == 0 and any("no data rows" in p for p in problems), "header only: %r" % (problems,))
            checks.append("header-only case fails with no data rows")

            ok, problems, row_count, _ = mod.check_file(os.path.join(tmp, "nope.csv"))
            check(not ok and any("not found" in p for p in problems), "missing file: %r" % (problems,))
            checks.append("missing file fails with not found")

            custom = write_csv(tmp, "custom.csv", ["name", "source"], [["A", "https://example.org/a"]])
            ok, problems, row_count, _ = mod.check_file(custom, expected_columns=["name", "source"], url_column="source")
            check(ok and row_count == 1, "custom schema: %r" % (problems,))
            checks.append("custom --columns schema passes")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["csv_schema_check.py", good])
            out = buf.getvalue()
            check(code == 0 and "PASS:" in out and "(2 rows" in out, "CLI valid: %r %r" % (code, out))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["csv_schema_check.py", empty_field])
            out = buf.getvalue()
            check(code == 1 and "FAIL:" in out and "(2 rows)" in out, "CLI fail: %r %r" % (code, out))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["csv_schema_check.py", custom, "--columns", "name,source"])
            check(code == 0 and "PASS:" in buf.getvalue(), "CLI custom: %r %r" % (code, buf.getvalue()))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["csv_schema_check.py"])
            check(code == 1 and "usage" in buf.getvalue(), "CLI no args: %r %r" % (code, buf.getvalue()))
            checks.append("CLI exits 0 with PASS, 1 with FAIL, handles custom columns and no args")
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
