# agent-memory-lint-fixtures-run

A self-contained test fixture and self-test for the JSONL memory record lint checker.

## How to run

```sh
python3 self_test.py
```

The first run captures the real stdout and exit code of `lint.py` on the
`fixtures/tiny_memory.jsonl` fixture into `fixtures/expected_out.txt`
and `fixtures/expected_exit.txt`.

Subsequent runs compare the current output byte-for-byte with those
captured files and print a `PASS` line for each verification, including
the raw command executed.

All paths are resolved relative to the location of `self_test.py`, so the
folder can be moved or copied freely. No network access is used.
