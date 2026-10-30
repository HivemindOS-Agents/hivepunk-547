#!/usr/bin/env python3
"""Self-test for preflight_csv.py.

Runs four test cases:
1. good.csv – passes all four rules.
2. bad_header.csv – header does not match expected.
3. bad_fields.csv – one row has wrong field count.
4. bad_quality.csv – empty field and leading/trailing whitespace.

Exits 0 only if every case produces the expected output and exit code.
"""

import sys
import tempfile
import os
import subprocess

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_PATH = os.path.join(TEST_DIR, 'preflight_csv.py')

# ------------------------------------------------------------
# Helper: write a CSV string to a temp file and run the script
# ------------------------------------------------------------
def run_test(content, expected_header):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(content)
        f.flush()
        path = f.name
    try:
        cp = subprocess.run(
            [sys.executable, SCRIPT_PATH, path, expected_header],
            capture_output=True,
            text=True
        )
    finally:
        os.unlink(path)
    return cp

# ------------------------------------------------------------
# Test data
# ------------------------------------------------------------
GOOD_CSV = """a,b,c
1,2,3
x,y,z
"""
GOOD_HEADER = "a,b,c"

BAD_HEADER_CSV = """a,b,d
1,2,3
"""
BAD_HEADER_EXPECTED = "a,b,c"

BAD_FIELDS_CSV = """a,b,c
1,2,3,4
"""
BAD_FIELDS_HEADER = "a,b,c"

BAD_QUALITY_CSV = """a,b,c
1,,3
 4,5,6
"""
BAD_QUALITY_HEADER = "a,b,c"

# ------------------------------------------------------------
# Asserts
# ------------------------------------------------------------
all_pass = True

# Case 1: good file
try:
    cp = run_test(GOOD_CSV, GOOD_HEADER)
    expected_stdout = """header_match: PASS
field_count_consistency: PASS
no_empty_required: PASS
no_stray_whitespace: PASS
"""
    if cp.returncode != 0:
        print(f"FAIL (good): exit {cp.returncode}, expected 0")
        all_pass = False
    elif cp.stdout != expected_stdout:
        print(f"FAIL (good): stdout mismatch")
        print(f"  got:\n{cp.stdout}")
        print(f"  expected:\n{expected_stdout}")
        all_pass = False
    else:
        print("PASS: good.csv")
except Exception as e:
    print(f"FAIL (good): exception {e}")
    all_pass = False

# Case 2: bad header
cp = run_test(BAD_HEADER_CSV, BAD_HEADER_EXPECTED)
if cp.returncode != 1:
    print(f"FAIL (bad_header): exit {cp.returncode}, expected 1")
    all_pass = False
else:
    if 'header_match: FAIL' in cp.stdout:
        print("PASS: bad_header.csv")
    else:
        print(f"FAIL (bad_header): stdout missing expected FAIL:\n{cp.stdout}")
        all_pass = False

# Case 3: bad field count
cp = run_test(BAD_FIELDS_CSV, BAD_FIELDS_HEADER)
if cp.returncode != 1:
    print(f"FAIL (bad_fields): exit {cp.returncode}, expected 1")
    all_pass = False
else:
    if 'field_count_consistency: FAIL' in cp.stdout:
        print("PASS: bad_fields.csv")
    else:
        print(f"FAIL (bad_fields): stdout missing expected FAIL:\n{cp.stdout}")
        all_pass = False

# Case 4: bad quality (empty and whitespace)
cp = run_test(BAD_QUALITY_CSV, BAD_QUALITY_HEADER)
if cp.returncode != 1:
    print(f"FAIL (bad_quality): exit {cp.returncode}, expected 1")
    all_pass = False
else:
    has_empty_fail = 'no_empty_required: FAIL' in cp.stdout
    has_stray_fail = 'no_stray_whitespace: FAIL' in cp.stdout
    if has_empty_fail and has_stray_fail:
        print("PASS: bad_quality.csv")
    else:
        print(f"FAIL (bad_quality): stdout missing expected FAILs:\n{cp.stdout}")
        all_pass = False

# ------------------------------------------------------------
sys.exit(0 if all_pass else 1)
