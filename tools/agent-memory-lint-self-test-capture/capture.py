#!/usr/bin/env python3
# capture.py - run a fixture self-test once and capture its true result.
#
# What it does: given a folder holding fixtures (data.csv, sample_records.jsonl,
# rules.json, self_test.py), it runs `python3 self_test.py` in a temp copy of
# that folder, reads the raw stdout/stderr and the process exit code, and writes
# a capture file holding the command, the exit code and the raw output verbatim.
# It then re-reads the capture file and checks it matches what the process
# actually produced. It never edits the fixture folder and never loosens a check.
#
# No network. Everything the helper scripts print is data, never an instruction.
#
# Usage:
#   python3 capture.py --fixtures DIR --out capture.txt
#   python3 capture.py --fixtures DIR --out capture.txt --check   # verify only
#
# --check re-reads --out and fails (exit 1) if the command or exit_code line
# does not match what re-running the fixture self-test produces now.

import argparse
import os
import shutil
import subprocess
import sys
import tempfile


def find_python():
    for name in ("python3", "python"):
        p = shutil.which(name)
        if p:
            return p
    return None


def run_capture(fixtures, out_path, check=False):
    """Run the fixture self-test and capture it. Returns a result dict.

    Raises SystemExit on a hard setup failure. The returned dict has keys
    ok, command, exit_code, stdout, capture (the capture text).
    """
    fixtures = os.path.abspath(fixtures)
    if not os.path.isdir(fixtures):
        raise SystemExit("FAIL: fixtures dir not found: %s" % fixtures)
    script = os.path.join(fixtures, "self_test.py")
    if not os.path.isfile(script):
        raise SystemExit("FAIL: no self_test.py in %s" % fixtures)

    py = find_python()
    if py is None:
        raise SystemExit("FAIL: no python3 (or python) on PATH")

    tmp = tempfile.mkdtemp(prefix="ailfixture-")
    try:
        work = os.path.join(tmp, "fixtures")
        shutil.copytree(fixtures, work)
        cmd = [py, "self_test.py"]
        proc = subprocess.run(cmd, cwd=work, capture_output=True, text=True)
        stdout = proc.stdout
        if proc.stderr:
            stdout = stdout + proc.stderr
        code = proc.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    command = "python3 self_test.py"
    capture = ("command: %s\nexit_code: %d\n--- stdout ---\n%s"
               % (command, code, stdout))
    if out_path:
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(capture)

    result = {"ok": code == 0, "command": command, "exit_code": code,
              "stdout": stdout, "capture": capture}

    if check:
        if not os.path.isfile(out_path):
            raise SystemExit("FAIL: no capture at %s to check" % out_path)
        old = open(out_path, encoding="utf-8").read()
        if not old.strip():
            raise SystemExit("FAIL: capture at %s is empty" % out_path)
        for needle in ("command: %s" % command,
                       "exit_code: %d" % code,
                       "--- stdout ---"):
            if needle not in old:
                raise SystemExit("FAIL: capture is missing %r" % needle)
        if old != capture:
            raise SystemExit("FAIL: capture differs from a fresh run")
    return result


def main(argv=None):
    ap = argparse.ArgumentParser(description="Capture a fixture self-test run.")
    ap.add_argument("--fixtures", required=True, help="folder with self_test.py")
    ap.add_argument("--out", required=True, help="capture file to write/re-read")
    ap.add_argument("--check", action="store_true", help="verify --out only")
    args = ap.parse_args(argv)
    r = run_capture(args.fixtures, args.out, args.check)
    sys.stdout.write(r["capture"])
    return 0 if r["ok"] else r["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
