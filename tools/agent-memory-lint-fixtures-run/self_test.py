#!/usr/bin/env python3
"""Self-test for tools/agent-memory-lint-fixtures-run.

Builds all paths from ``Path(__file__).parent``.  Runs the folder's
``lint.py`` on ``fixtures/tiny_memory.jsonl`` via subprocess (no network,
no spend).

- On the first run, captures ``lint.py``'s real stdout to
  ``fixtures/expected_out.txt`` and exit code to
  ``fixtures/expected_exit.txt``.
- On later runs, asserts both are byte-identical, printed with captured
  bytes and the raw command.
- Exits 0 only when every check passes.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
FIXTURE = FIXTURES / "tiny_memory.jsonl"
LINT = HERE / "lint.py"
EXPECTED_OUT = FIXTURES / "expected_out.txt"
EXPECTED_EXIT = FIXTURES / "expected_exit.txt"

TIMEOUT = 30
COMMAND = f"python3 {LINT.name} {FIXTURE.relative_to(HERE)}"


def fail(message: str) -> int:
    print(f"FAIL {message}")
    return 1


def main() -> int:
    for p in (FIXTURE, LINT):
        if not p.is_file():
            return fail(f"missing {p.relative_to(HERE)}")

    env = os.environ.copy()
    env["PYTHONNOUSERSITE"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.pop("PYTHONPATH", None)

    try:
        proc = subprocess.run(
            [sys.executable, str(LINT), str(FIXTURE)],
            cwd=str(HERE),
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return fail(f"lint.py timed out after {TIMEOUT}s")
    except OSError as exc:
        return fail(f"could not run lint.py: {exc}")

    actual_stdout = proc.stdout
    actual_exit = f"{proc.returncode}\n".encode("utf-8")

    # On the first run, capture expected files.
    FIXTURES.mkdir(parents=True, exist_ok=True)
    first_run = not EXPECTED_OUT.exists() or not EXPECTED_EXIT.exists()
    if first_run:
        EXPECTED_OUT.write_bytes(actual_stdout)
        EXPECTED_EXIT.write_bytes(actual_exit)
        print(f"CAPTURED stdout -> fixtures/expected_out.txt ({len(actual_stdout)} bytes): {actual_stdout!r}")
        print(f"CAPTURED exit -> fixtures/expected_exit.txt ({len(actual_exit)} bytes): {actual_exit!r}")

    # Read expected files (may have been written just above).
    expected_stdout = EXPECTED_OUT.read_bytes()
    expected_exit = EXPECTED_EXIT.read_bytes()

    ok = True

    if actual_exit != expected_exit:
        print(f"FAIL exit code: expected {expected_exit!r}, got {actual_exit!r}")
        ok = False
    else:
        print(f"PASS exit code matches fixtures/expected_exit.txt ({len(actual_exit)} bytes): {actual_exit!r}")
        print(f"  raw command: {COMMAND}")

    if actual_stdout != expected_stdout:
        print(f"FAIL stdout: expected {expected_stdout!r}, got {actual_stdout!r}")
        ok = False
    else:
        print(f"PASS stdout byte-identical to fixtures/expected_out.txt ({len(actual_stdout)} bytes): {actual_stdout!r}")
        print(f"  raw command: {COMMAND}")

    if proc.stderr:
        print(f"NOTE lint.py stderr ({len(proc.stderr)} bytes): {proc.stderr!r}")

    print("PASS fixture read from ./fixtures/tiny_memory.jsonl only")
    if not ok:
        return 1
    print("OK self-test passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
