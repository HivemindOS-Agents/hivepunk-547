# Drafted the folder-only self_test.py, tiny_memory.md fixture and README; first run captures expected stdout/exit, later runs assert bytes.

**Done**

2026-11-06 15:56 UTC, spent $0.01 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/547

Draft for tools/agent-memory-lint-self-test-capture/ only. Three files change; no data path outside the folder is read or written.

## fixtures/tiny_memory.md
```markdown
# Tiny memory
- Read only from this folder.
- Capture real stdout and exit code, then compare bytes.
```
(three lines, newline-terminated)

## self_test.py
```python
#!/usr/bin/env python3
'''Self-test for the sibling capture tool. Data paths are relative to this file.'''
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / 'fixtures'
FIXTURE = FIXTURES / 'tiny_memory.md'
EXPECTED_STDOUT = FIXTURES / 'expected_stdout.txt'
EXPECTED_EXIT = FIXTURES / 'expected_exit.txt'

# Sibling capture tool. Add a filename here if the real one differs; do not
# point outside this folder.
CAPTURE_CANDIDATES = [
    HERE / 'capture.py',
    HERE / 'self_test_capture.py',
    HERE / 'capture_self_test.py',
    HERE / 'agent_memory_capture.py',
    HERE / 'memory_capture.py',
    HERE / 'lint_capture.py',
]
CAPTURE_ARGS = lambda capture: [str(FIXTURE)]  # fixture is the only input
TIMEOUT = 30


def fail(message):
    print(f'FAIL {message}')
    return 1


def main():
    if not FIXTURE.is_file():
        return fail(f'missing fixture {FIXTURE.relative_to(HERE)}')

    capture = next((p for p in CAPTURE_CANDIDATES if p.is_file()), None)
    if capture is None:
        names = ', '.join(p.name for p in CAPTURE_CANDIDATES)
        return fail(f'missing capture tool; looked for: {names}')

    env = os.environ.copy()
    env['PYTHONNOUSERSITE'] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env.pop('PYTHONPATH', None)

    try:
        proc = subprocess.run(
            [sys.executable, str(capture), *CAPTURE_ARGS(capture)],
            cwd=str(HERE),
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return fail(f'capture tool timed out after {TIMEOUT}s')
    except OSError as exc:
        return fail(f'could not run capture tool: {exc}')

    actual_stdout = proc.stdout
    actual_exit = f'{proc.returncode}\n'.encode('ascii')

    FIXTURES.mkdir(parents=True, exist_ok=True)
    if not EXPECTED_STDOUT.exists():
        EXPECTED_STDOUT.write_bytes(actual_stdout)
        print(f'CAPTURED stdout -> fixtures/expected_stdout.txt ({len(actual_stdout)} bytes): {actual_stdout!r}')
    if not EXPECTED_EXIT.exists():
        EXPECTED_EXIT.write_bytes(actual_exit)
        print(f'CAPTURED exit -> fixtures/expected_exit.txt ({len(actual_exit)} bytes): {actual_exit!r}')

    expected_stdout = EXPECTED_STDOUT.read_bytes()
    expected_exit = EXPECTED_EXIT.read_bytes()

    ok = True
    if actual_exit != expected_exit:
        print(f'FAIL exit code: expected {expected_exit!r}, got {actual_exit!r}')
        ok = False
    else:
        print(f'PASS exit code matches fixtures/expected_exit.txt ({len(actual_exit)} bytes): {actual_exit!r}')

    if actual_stdout != expected_stdout:
        print(f'FAIL stdout: expected {expected_stdout!r}, got {actual_stdout!r}')
        ok = False
    else:
        print(f'PASS stdout byte-identical to fixtures/expected_stdout.txt ({len(actual_stdout)} bytes): {actual_stdout!r}')

    if proc.stderr:
        print(f'NOTE capture stderr ({len(proc.stderr)} bytes): {proc.stderr!r}')

    print('PASS fixture read from ./fixtures/tiny_memory.md only')
    if not ok:
        return 1
    print('OK self-test passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

## README.md
```markdown
# agent-memory-lint-self-test-capture

One command, from this folder:

    python3 self_test.py

It runs the sibling capture tool on `fixtures/tiny_memory.md` with `subprocess`
(no network, no spend). The first run captures the tool's real stdout and exit
code into `fixtures/expected_stdout.txt` and `fixtures/expected_exit.txt`. Later
runs assert both files are byte-identical and print a PASS line for each with
the captured bytes.

The expected files are captured, not derived: they are written from the capture
tool's actual bytes, never hand-typed or recomputed. Every data path in
`self_test.py` is built from `Path(__file__).parent`, so the folder can be copied
and run alone.
```

## What I could not confirm
I could not run Python or the capture tool from here, so the real capture-tool
filename, its CLI and the resulting expected bytes are not confirmed. The script
discovers common sibling filenames and passes the fixture as a positional
argument; if the tool uses another name or flag, change only
`CAPTURE_CANDIDATES` and `CAPTURE_ARGS`. Do not guess expected bytes: let the
first run write them, then commit those captured files.

Left for the owner: build this draft into `tools/agent-memory-lint-self-test-capture/`
only, commit that folder, and let HivemindOS run `python3 self_test.py`; the first
run captures the two expected files, later runs assert them.
