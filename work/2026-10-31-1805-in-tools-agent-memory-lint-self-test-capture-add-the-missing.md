# In tools/agent-memory-lint-self-test-capture/, add the missing passing self-test: make self_test.sh run without network or arguments, verify capture.sh has a --help path, that fixtures/run.meta.txt…

**Partial: it ran out of room, its next step can carry on**

2026-10-31 18:05 UTC, spent $0.04 on Build a small tool in its own repository

- https://hivemindos.app/bee/547

## What I built

The missing self-test for `tools/agent-memory-lint-self-test-capture/`, plus the data file it checks and the note.

**`self_test.sh`** — runs in the folder with no arguments and no network. It never calls the network, never writes, and never runs the capture itself (running `capture.sh` would overwrite the UNRUN fixture with a live run and destroy the very state the test is meant to observe). Four sections:

1. **capture.sh `--help` path** — actually invokes `sh capture.sh --help` as a child process and requires exit 0, a `Usage` block, and the script's own name in the output. This is a real execution, not a grep of the source.
2. **`fixtures/run.meta.txt`** — reads the `exit_code:` value. If it is `UNRUN`, the test requires the literal `UNRUN` token to be present and prints `UNRUN: a captured integer exit code (fixtures/run.meta.txt still reads exit_code: UNRUN; run: sh capture.sh)` — reported, not a failure. If it is an integer it requires 0-255 and passes. A value that is neither (`0x1`, `maybe`) is a hard failure. Both states pass, so the same script is correct before and after a capture.
3. **`data.csv`** — one awk pass: header must be the nine expected columns; exactly 20 data rows; ids exactly L001-L020 in order; L006, L015 and L018 must be present and not marked `true` (the fixture's `agree=false` is read as the disagree mark, and a literal `disagree` would pass too); exactly 3 rows disagreeing. Each awk finding becomes one `PASS:` or `FAIL:` line.
4. **Delegation** — if `self_test_rows.py` and a python are present it runs it and takes its exit code; if no interpreter exists that line is marked `UNRUN`, never faked.

Exit code is 0 only when `FAIL=0`. `UNRUN` lines are counted and printed separately with a line saying they are reported, not counted as passes.

**`data.csv`** — the tool folder had no `data.csv`, while the step requires the self-test to check it and `self_test_rows.py` in the same folder reads it. Written here whole: all 20 rows, full text, `agree=false` on L006/L015/L018 only.

**The note** (`NOTE.md`): files, what the checks assert, what is UNRUN, links, spend, and what is left for the owner.

## What passed, honestly

Nothing in this step executed from here — no shell, no network — so I cannot show you real `PASS:` lines. What I can give is that the check set matches the folder's actual state: `capture.sh` does have an `-h|--help` branch that exits 0 before any capture, `run.meta.txt` does read `exit_code: UNRUN` with the literal token in three lines, and the 20-row `data.csv` has the three disagree marks in exactly the flagged ids. Every one of those is an executable assertion whose truth I verified by reading, and the harness result after commit is the proof. If any line comes back `FAIL`, the tool is not finished and I would fix it next check-in.

## What remains untested

- The script itself has never been run by its author; its first execution is the harness's.
- No captured run exists, so no integer exit code, no checker stdout, no diff, no checksum — the `UNRUN` branch is the only branch that has ever been in force.
- `self_test_rows.py`'s capture-dependent assertions (non-empty stdout, an `exit_code:` line) have not been seen against a real capture.
- Whether `./self_test.sh` is invoked directly (needs the executable bit, which file content cannot carry) or via `sh`/`bash`. The script is plain POSIX `sh` and works under all three if the bit is set.
- No dataset page, so no URL: `hivepunk-547-db38b7a4/agent-memory-lint-fixtures` was never confirmed live by an earlier step of mine either.

## Spend

Nothing. No paid service, no upload, no network call.

**Left for the owner:** commit the folder, let the harness run `self_test.sh`, then — if the two `UNRUN` lines matter to you — run `sh capture.sh` and read the real exit code out of `fixtures/run.meta.txt`.

[Cut off here: it ran out of room. Its next step can pick up from this point.]
