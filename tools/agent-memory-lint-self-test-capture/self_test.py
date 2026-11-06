#!/usr/bin/env python3
"""Self‑test harness for the folder’s capture tool.

*  All paths are derived from the location of this file.
*  The suite looks for a Python capture script in the same directory
   that accepts a single positional argument – the path of the memory
   fixture – and prints a JSON‑ready output.
*  On the first run the real stdout and exit code are written to
   ``fixtures/expected_stdout.txt`` and ``fixtures/expected_exit.txt``.
*  On later runs the expected files are read and the captured values
   are byte‑identical to them; any mismatch causes a non‑zero exit.
*  The script prints a PASS line for each successful check.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
FIXTURE = FIXTURES / "tiny_memory.md"
EXPECTED_STDOUT = FIXTURES / "expected_stdout.txt"
EXPECTED_EXIT = FIXTURES / "expected_exit.txt"

# Candidate capture scripts – the suite will pick the first existing one.
# The name is deliberately generic so that the folder can ship any name
# that exposes the required CLI contract.
CAPTURE_CANDIDATES = [
    HERE / "capture.py",
    HERE / "capture_self_test.py",
    HERE / "agent_memory_capture.py",
    HERE / "memory_capture.py",
    HERE / "lint_capture.py",
    HERE / "agent-memory-capture.py",
]

# The capture tool must be a Python module that outputs to stdout.
# We invoke it with the fixture path as a single argument.
CAPTURE_ARGS = lambda capture: [str(FIXTURE)]
TIMEOUT = 30


def fail(msg: str) -> int:
    print(f"FAIL {msg}")
    return 1


def main() -> int:
    if not FIXTURE.is_file():
        return fail(f"missing fixture {FIXTURE.relative_to(HERE)}")

    capture = next((p for p in CAPTURE_CANDIDATES if p.is_file()), None)
    if capture is None:
        names = ", ".join(p.name for p in CAPTURE_CANDIDATES)
        return fail(f"missing capture tool; looked for: {names}")

    # Prepare environment that **doesn’t** import a global PYTHONPATH.
    env = os.environ.copy()
    env["PYTHONNOUSERSITE"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.pop("PYTHONPATH", None)

    try:
        result = subprocess.run(
            [sys.executable, str(capture), *CAPTURE_ARGS(capture)],
            cwd=str(HERE),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return fail(f"capture tool timed out after {TIMEOUT}s")
    except OSError as exc:
        return fail(f"could not run capture tool: {exc}")

    actual_stdout = result.stdout
    actual_exit = f"{result.returncode}\n".encode("utf-8")

    # Ensure the fixture directory exists.
    FIXTURES.mkdir(parents=True, exist_ok=True)

    # On the first run, write the expected bytes.
    first_run = not EXPECTED_STDOUT.exists() or not EXPECTED_EXIT.exists()
    if first_run:
        EXPECTED_STDOUT.write_bytes(actual_stdout)
        EXPECTED_EXIT.write_bytes(actual_exit)
        print(f"CAPTURED stdout -> fixtures/expected_stdout.txt ({len(actual_stdout)} bytes): {actual_stdout!r}")
        print(f"CAPTURED exit -> fixtures/expected_exit.txt ({len(actual_exit)} bytes): {actual_exit!r}")

    expected_stdout = EXPECTED_STDOUT.read_bytes()
    expected_exit = EXPECTED_EXIT.read_bytes()

    ok = True
    if actual_exit != expected_exit:
        print(f"FAIL exit code: expected {expected_exit!r}, got {actual_exit!r}")
        ok = False
    else:
        print(f"PASS exit code matches fixtures/expected_exit.txt ({len(actual_exit)} bytes): {actual_exit!r}")

    if actual_stdout != expected_stdout:
        print(f"FAIL stdout: expected {expected_stdout!r}, got {actual_stdout!r}")
        ok = False
    else:
        print(f"PASS stdout byte-identical to fixtures/expected_stdout.txt ({len(actual_stdout)} bytes): {actual_stdout!r}")

    if proc := result:  # capture stderr for annotation
        if proc.stderr:
            print(f"NOTE capture stderr ({len(proc.stderr)} bytes): {proc.stderr!r}")

    print("PASS fixture read from ./fixtures/tiny_memory.md only")
    if not ok:
        return 1
    print("OK self-test passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
