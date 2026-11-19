#!/usr/bin/env python3
"""kinematics_check.py: flag DH-parameter and unit inconsistencies in CSVs.

Usage (from this folder):
    python3 kinematics_check.py joints.csv
    python3 kinematics_check.py joints.csv -o REPORT.txt

One stated row format (header required, any order tolerated):
    joint_index,joint_type,link_length_a,link_twist_alpha,link_offset_d,theta_offset,length_unit,angle_unit

Stated rules only -- this is a consistency checker, not a full
kinematics solver and it does not verify a real robot:
    - all eight columns present, no extra columns
    - joint_index is an integer, starting at 1 and increasing by 1
    - joint_type is revolute or prismatic
    - link_length_a, link_twist_alpha, link_offset_d and theta_offset
      are finite numbers (nan/inf rejected)
    - link_length_a >= 0
    - link_twist_alpha within its angle unit: |alpha| <= 180 deg or
      <= pi rad; theta_offset within |theta| <= 360 deg or <= 2*pi rad
    - length_unit is m, mm or cm; angle_unit is deg or rad
    - unit consistency: every row must use the same length_unit and
      the same angle_unit as the first data row; mixed units are flagged
    - blank lines are skipped and counted; no extra/missing fields

Read-only, no network. Exit 0 PASS, 1 problems/bad input, 2 usage.
"""

import csv
import math
import os
import sys

REQUIRED = (
    "joint_index", "joint_type", "link_length_a", "link_twist_alpha",
    "link_offset_d", "theta_offset", "length_unit", "angle_unit",
)
NUMERIC = ("link_length_a", "link_twist_alpha", "link_offset_d", "theta_offset")
LENGTH_UNITS = ("m", "mm", "cm")
ANGLE_UNITS = ("deg", "rad")
JOINT_TYPES = ("revolute", "prismatic")
EPS = 1e-9


def parse_number(text):
    try:
        value = float(text)
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def angle_limit(angle_unit, kind):
    if kind == "alpha":
        return 180.0 if angle_unit == "deg" else math.pi
    return 360.0 if angle_unit == "deg" else 2.0 * math.pi


def check_rows(rows):
    """rows: list of dicts with _line. Return (valid_count, problems)."""
    problems = []
    valid = 0
    expected_index = 1
    first_length_unit = None
    first_angle_unit = None
    for row in rows:
        line = row.get("_line", "?")
        bad = False

        def fail(msg):
            nonlocal bad
            problems.append("line %s: %s" % (line, msg))
            bad = True

        vals = {k: str(row.get(k, "") or "").strip() for k in REQUIRED}
        for k in REQUIRED:
            if not vals[k]:
                fail("empty %s" % k)
        # joint_index: integer and sequential from 1.
        idx = None
        if vals["joint_index"]:
            try:
                idx = int(vals["joint_index"])
            except ValueError:
                fail("joint_index is not an integer: %r" % vals["joint_index"])
            if idx is not None:
                if idx != expected_index:
                    fail("joint_index %d out of sequence (expected %d)" % (idx, expected_index))
                expected_index = idx + 1
        if vals["joint_type"] and vals["joint_type"].lower() not in JOINT_TYPES:
            fail("unknown joint_type %r (allowed: %s)" % (vals["joint_type"], ", ".join(JOINT_TYPES)))
        # units and cross-row consistency.
        length_unit = vals["length_unit"].lower()
        angle_unit = vals["angle_unit"].lower()
        if vals["length_unit"] and length_unit not in LENGTH_UNITS:
            fail("unknown length_unit %r (allowed: %s)" % (vals["length_unit"], ", ".join(LENGTH_UNITS)))
        if vals["angle_unit"] and angle_unit not in ANGLE_UNITS:
            fail("unknown angle_unit %r (allowed: %s)" % (vals["angle_unit"], ", ".join(ANGLE_UNITS)))
        if length_unit in LENGTH_UNITS:
            if first_length_unit is None:
                first_length_unit = length_unit
            elif length_unit != first_length_unit:
                fail("length_unit %r inconsistent with first row %r" % (length_unit, first_length_unit))
        if angle_unit in ANGLE_UNITS:
            if first_angle_unit is None:
                first_angle_unit = angle_unit
            elif angle_unit != first_angle_unit:
                fail("angle_unit %r inconsistent with first row %r" % (angle_unit, first_angle_unit))
        # numeric DH values and ranges.
        nums = {}
        for k in NUMERIC:
            if vals[k]:
                nums[k] = parse_number(vals[k])
                if nums[k] is None:
                    fail("%s is not a finite number: %r" % (k, vals[k]))
                else:
                    nums[k] = nums[k]
        if nums.get("link_length_a") is not None and nums["link_length_a"] < 0:
            fail("link_length_a is negative: %s" % vals["link_length_a"])
        if angle_unit in ANGLE_UNITS:
            alpha = nums.get("link_twist_alpha")
            if alpha is not None and abs(alpha) > angle_limit(angle_unit, "alpha") + EPS:
                fail("link_twist_alpha %s out of range for %s (limit %s)" % (vals["link_twist_alpha"], angle_unit, angle_limit(angle_unit, "alpha")))
            theta = nums.get("theta_offset")
            if theta is not None and abs(theta) > angle_limit(angle_unit, "theta") + EPS:
                fail("theta_offset %s out of range for %s (limit %s)" % (vals["theta_offset"], angle_unit, angle_limit(angle_unit, "theta")))
        if not bad:
            valid += 1
    return valid, problems


def load_csv(path):
    """Return (rows, problems, skipped_blank)."""
    problems = []
    rows = []
    skipped = 0
    with open(path, encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        try:
            raw_header = next(reader)
        except StopIteration:
            return [], ["missing header (expected %s)" % ",".join(REQUIRED)], 0
        headers = [h.strip() for h in raw_header]
        missing = [c for c in REQUIRED if c not in headers]
        extra = [h for h in headers if h and h not in REQUIRED]
        if missing:
            problems.append("missing column(s): %s" % ", ".join(missing))
        if extra:
            problems.append("unexpected column(s): %s" % ", ".join(extra))
        if problems:
            return [], problems, 0
        index = {name: headers.index(name) for name in REQUIRED}
        for lineno, raw in enumerate(reader, 2):
            if not raw or all(not str(v).strip() for v in raw):
                skipped += 1
                continue
            if len(raw) > len(headers):
                problems.append("line %d: extra fields beyond header" % lineno)
                continue
            vals = {k: (raw[index[k]] if index[k] < len(raw) else "") for k in REQUIRED}
            vals["_line"] = lineno
            rows.append(vals)
    if not rows and not problems:
        problems.append("no data rows found")
    return rows, problems, skipped


def check_file(path):
    if not os.path.exists(path):
        return None, ["input file not found: %s" % path], 0
    if not os.path.isfile(path):
        return None, ["input path is not a file: %s" % path], 0
    try:
        rows, problems, skipped = load_csv(path)
    except (OSError, UnicodeError) as e:
        return None, ["could not read input: %s: %s" % (type(e).__name__, e)], 0
    except csv.Error as e:
        return None, ["invalid CSV: %s" % e], 0
    if problems and not rows:
        return {"total": 0, "valid": 0, "rows": []}, problems, skipped
    valid, row_problems = check_rows(rows)
    problems.extend(row_problems)
    return {"total": len(rows), "valid": valid, "rows": rows}, problems, skipped


def main(argv):
    args = list(argv[1:])
    input_path = None
    output_path = None
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("-o", "--output"):
            if i + 1 >= len(args):
                print("FAIL: %s needs a value" % arg)
                return 2
            output_path = args[i + 1]
            i += 2
        elif arg in ("-h", "--help"):
            print(__doc__.strip())
            return 0
        elif arg.startswith("--"):
            print("FAIL: unknown option %s" % arg)
            return 2
        elif input_path is None:
            input_path = arg
            i += 1
        else:
            print("FAIL: unexpected extra argument %s" % arg)
            return 2
    if not input_path:
        print("FAIL: usage: python3 kinematics_check.py joints.csv [-o REPORT.txt]")
        return 2
    report, problems, skipped = check_file(input_path)
    if report is None:
        for p in problems:
            print("FAIL: %s: %s" % (input_path, p))
        return 1
    if skipped:
        print("NOTE: skipped %d blank row(s)" % skipped, file=sys.stderr)
    lines = ["counts: total=%d valid=%d problems=%d" % (report["total"], report["valid"], len(problems))]
    if problems:
        lines.extend("FAIL: %s: %s" % (input_path, p) for p in problems)
        lines.append("FAIL: %s (problems: %d)" % (input_path, len(problems)))
        code = 1
    else:
        lines.append("PASS: %s (rows: %d)" % (input_path, report["total"]))
        code = 0
    text = "\n".join(lines) + "\n"
    if output_path:
        try:
            with open(output_path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
        except OSError as e:
            print("FAIL: could not write output: %s: %s" % (type(e).__name__, e))
            return 1
        print("wrote report to %s" % output_path)
    else:
        sys.stdout.write(text)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
