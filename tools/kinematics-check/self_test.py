#!/usr/bin/env python3
"""Self-test for kinematics-check. No args, no network."""

import contextlib
import io
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HEADER = "joint_index,joint_type,link_length_a,link_twist_alpha,link_offset_d,theta_offset,length_unit,angle_unit\n"
GOOD = HEADER + "1,revolute,0.3,-1.5708,0.1,0,m,rad\n2,revolute,0.25,0,0.05,1.5708,m,rad\n"


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
        return __import__("kinematics_check")
    except Exception as e:
        raise Fail("could not import kinematics_check: %s: %s" % (type(e).__name__, e))


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


def check_text(mod, text):
    with tempfile.TemporaryDirectory() as tmp:
        return mod.check_file(write(tmp, "in.csv", text))


def main():
    try:
        mod = import_tool()
        checks = []
        report, problems, _ = check_text(mod, GOOD)
        check(problems == [] and report["total"] == 2 and report["valid"] == 2, "good: %r" % (problems,))
        checks.append("consistent m/rad rows pass")

        deg = HEADER + "1,prismatic,300,90,50,180,mm,deg\n2,revolute,200,-90,0,-180,mm,deg\n"
        report, problems, _ = check_text(mod, deg)
        check(problems == [] and report["valid"] == 2, "deg/mm: %r" % (problems,))
        checks.append("consistent mm/deg boundary values pass")

        mixed = HEADER + "1,revolute,0.3,0,0.1,0,m,rad\n2,revolute,300,0,50,0,mm,deg\n"
        report, problems, _ = check_text(mod, mixed)
        check(any("length_unit" in p and "inconsistent" in p for p in problems), "mixed length: %r" % (problems,))
        check(any("angle_unit" in p and "inconsistent" in p for p in problems), "mixed angle: %r" % (problems,))
        checks.append("mixed length and angle units flagged")

        bad = HEADER + "2,rotary,-0.3,3.5,0.1,7.0,ft,rad\n"
        report, problems, _ = check_text(mod, bad)
        joined = " ".join(problems)
        for needle in ("out of sequence", "joint_type", "negative", "out of range", "length_unit"):
            check(needle in joined, "bad row missing %r: %r" % (needle, problems))
        checks.append("bad index/type/negative/range/unit flagged")

        nonnum = HEADER + "1,revolute,abc,nan,0.1,inf,m,rad\n"
        report, problems, _ = check_text(mod, nonnum)
        check(len([p for p in problems if "not a finite number" in p]) == 3, "nonnum: %r" % (problems,))
        checks.append("non-numeric, nan and inf flagged")

        report, problems, _ = check_text(mod, "joint_index,joint_type\n1,revolute\n")
        check(any("missing column" in p for p in problems), "missing col: %r" % (problems,))
        report, problems, _ = check_text(mod, HEADER + "1,revolute,0.3,0,0.1,0,m,rad,extra\n")
        check(any("extra fields" in p for p in problems), "extra field: %r" % (problems,))
        report, problems, _ = check_text(mod, "")
        check(any("missing header" in p for p in problems), "empty: %r" % (problems,))
        report, problems, _ = check_text(mod, HEADER)
        check(any("no data rows" in p for p in problems), "no rows: %r" % (problems,))
        check(mod.parse_number("1.5") == 1.5 and mod.parse_number("nan") is None and mod.parse_number("x") is None, "parse_number")
        checks.append("missing/extra columns, empty and header-only fail clearly; parse_number works")

        with tempfile.TemporaryDirectory() as tmp:
            good_path = write(tmp, "good.csv", GOOD)
            code, out = run_main(mod, ["kinematics_check.py", good_path])
            check(code == 0 and "PASS:" in out, "CLI good: %r %r" % (code, out))
            bad_path = write(tmp, "bad.csv", mixed)
            code, out = run_main(mod, ["kinematics_check.py", bad_path])
            check(code == 1 and "FAIL:" in out, "CLI bad: %r %r" % (code, out))
            out_path = os.path.join(tmp, "REPORT.txt")
            code, out = run_main(mod, ["kinematics_check.py", good_path, "-o", out_path])
            check(code == 0 and os.path.exists(out_path), "CLI -o: %r %r" % (code, out))
            with open(out_path, encoding="utf-8") as fh:
                check("PASS:" in fh.read(), "-o contents")
            code, out = run_main(mod, ["kinematics_check.py", os.path.join(tmp, "nope.csv")])
            check(code == 1 and "not found" in out, "CLI missing: %r %r" % (code, out))
            code, out = run_main(mod, ["kinematics_check.py"])
            check(code == 2 and "usage" in out, "CLI usage: %r %r" % (code, out))
            checks.append("CLI exits 0 PASS, 1 FAIL/missing, 2 usage; -o writes report")
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
