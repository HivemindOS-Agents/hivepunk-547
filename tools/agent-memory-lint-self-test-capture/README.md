# agent-memory-lint-self-test-capture

A tiny, self‑contained self‑test that verifies the folder’s capture tool.

## How to run

```sh
python3 self_test.py
```

On the **first run** the harness captures the real stdout and exit code
returned by the capture tool into `fixtures/expected_stdout.txt` and
`fixtures/expected_exit.txt`.  On subsequent runs it compares the
actual output against those bytes and asserts they are byte‑identical.
The test prints a `PASS` line for each verification.  All paths are
resolved from `Path(__file__).parent`, so the folder can be moved or
copied without modification.

The expected output files are **captured from the tool’s execution**, not
hand‑typed or derived.
