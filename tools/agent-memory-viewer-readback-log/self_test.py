#!/usr/bin/env python3
"""Standalone self-test. No args, no network, run alone from this folder.
Imports agent_memory_rows, runs it on committed rows.csv and on
bad/sample rows, and compares outputs. Exit 0 only when all pass.
"""
import contextlib, io, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
try:
    import agent_memory_rows as tool
except Exception as e:
    sys.stderr.write("FAIL: import agent_memory_rows: %s\n" % e); sys.exit(1)
def check(c, m):
    if not c:
        sys.stderr.write("FAIL: %s\n" % m); sys.exit(1)
def run_cli(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): code = tool.main(argv)
    return code, buf.getvalue()
def main():
    checks = []
    rows, errs = tool.read_csv(os.path.join(HERE, "rows.csv"))
    check(errs == [], "rows.csv read errors %r" % (errs,))
    check(tool.validate(rows) == [], "rows.csv invalid: %r" % tool.validate(rows))
    check(len(rows) == 14, "expected 14 rows got %d" % len(rows))
    counts = {}
    for r in rows: counts[r[3]] = counts.get(r[3], 0) + 1
    check(counts == {"FACT": 6, "DERIVED": 4, "UNKNOWN": 4}, "label counts %r" % counts)
    check(tool.render(rows) == open(os.path.join(HERE, "rows.csv"), encoding="utf-8").read(), "render mismatch")
    checks.append("rows.csv validates (14 rows, FACT 6 DERIVED 4 UNKNOWN 4) and render round-trips")
    bad = [("", tool.SUBJECT, "c", "FACT", sorted(tool.ALLOWED)[0], tool.DATE), ("X", tool.SUBJECT, "c", "MAYBE", sorted(tool.ALLOWED)[0], tool.DATE), ("X", tool.SUBJECT, "c", "FACT", "ftp://x", tool.DATE), ("X", tool.SUBJECT, "c", "FACT", sorted(tool.ALLOWED)[0], "22-11-2026"), ("dup", tool.SUBJECT, "c", "FACT", sorted(tool.ALLOWED)[0], tool.DATE), ("dup", tool.SUBJECT, "c", "FACT", sorted(tool.ALLOWED)[0], tool.DATE)]
    joined = " ".join(tool.validate(bad))
    for needle in ("empty row_id", "unknown label", "not http(s)", "not YYYY-MM-DD", "duplicate row_id"):
        check(needle in joined, "validator missed %r in %s" % (needle, joined))
    checks.append("validator rejects empty id, bad label, off-scheme url, bad date, duplicate id")
    code, out = run_cli(["--check", os.path.join(HERE, "rows.csv")])
    check(code == 0 and "PASS: 14" in out, "CLI check %r %r" % (code, out))
    code, out = run_cli(["--bogus"])
    check(code == 2, "CLI bogus exit %r" % code)
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "rows.csv")
        with open(p, "w", encoding="utf-8") as fh: fh.write(tool.render(rows))
        code, out = run_cli(["--check", p]); check(code == 0, "temp CLI %r %r" % (code, out))
        with open(p, "a", encoding="utf-8") as fh: fh.write("EXTRA,%s,c,FACT,%s,%s\n" % (tool.SUBJECT, sorted(tool.ALLOWED)[0], tool.DATE))
        # extra row is still valid shape; check count change via validate only
        r2, e2 = tool.read_csv(p); check(len(r2) == 15 and tool.validate(r2) == [], "temp extra row")
    checks.append("CLI --check passes on committed and temp-clean copies, bogus arg exits 2")
    readme = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
    for needle in ("Caveats first", "FACT", "DERIVED", "UNKNOWN", "UNTESTED", "NOT confirmed", "ARTIFACTS.md log", "python3 self_test.py", "agent-memory-research-rows"):
        check(needle in readme, "README missing %r" % needle)
    checks.append("README has caveats, untested marks, intended URL and ARTIFACTS log")
    for line in checks: print(line)
    print("self-test: all checks passed")
    return 0
if __name__ == "__main__":
    sys.exit(main())
