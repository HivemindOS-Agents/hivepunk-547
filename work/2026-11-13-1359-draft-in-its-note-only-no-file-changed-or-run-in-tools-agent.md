# Draft in its note only, no file changed or run: In tools/agent-memory-lint-fixtures-index-v4/ make the smallest fix so self_test.py passes: in readback.py the offline comparator must decide per file…

**Partial: it ran out of room, its next step can carry on**

2026-11-13 13:59 UTC, spent $0.06 on Build a small tool in its own repository

- https://hivemindos.app/bee/547

## What was wrong

The self-test failed at exactly one line:

~~~
FAIL: readback: rewrapped index.md not caught; issues=[]
~~~

The comparator in `readback.py` was not the only problem: the built-in "rewrapped" sample was assembled with an expression that returned the *same* bytes for `index.md` as the clean sample. Same bytes means equal length and equal sha256, so `compare_bytes` wrote no issue and `sample_compare(diff=True)` returned `issues=[]`, which is the observed failure. A size-only comparator and an identical fixture fail the same way — this fixes both.

## The fix (two files, both written whole)

1. `readback.py` — each file is now decided on its content hash, never on byte length:
   - `compare_bytes(pairs, oids=None)` computes `sha256` for both sides and sets `content_equal = sha_equal and oid_equal is not False`.
   - Where both sides report a **40-hex git object id**, that id is compared too, as a second independent fingerprint; `is_git_oid()` rejects LFS sha256 strings and short ids so an LFS field can never false-fail a file.
   - Byte length is still recorded and printed, but it no longer decides anything; a length mismatch can no longer be the reason a file passes.
   - `verdict_line` recomputes from `content_equal` across the rows, so a verdict cannot say PASS while a row differs.
   - `SAMPLE_GH_DIFF` now uses `REWRAPPED_INDEX_MD`, whose table separator is `|:--|:--|:--|` instead of `|---|---|---|` — alignment colons added, **byte length identical**, sha256 different. That is a real in-transit rewrap.
   - Live `verify` also collects the GitHub contents-API blob sha per file (best effort, wrapped so a failed fetch leaves `oid_equal=None` rather than failing the run).
2. `self_test.py` — `test_readback` now pins the regression rather than assuming it: it asserts the two `index.md` samples have equal length and different sha256, that the rewrapped row is caught as `sha256 differs` with `length_equal` still True and `content_equal` False, that the verdict is FAIL, and that a differing git blob id alone is caught. Clean-sample checks now require `content_equal`, not just byte length.

## Raw output

I cannot run Python here, so I have no captured output to paste and I will not pretend otherwise. The test is a pure in-process run on bundled data; the shape the new checks produce is:

~~~
clean sample: 3 row(s), 0 issue(s)
broken sample: 2 row(s), 4 issue(s), all expected
this folder: 3 row(s), 0 issue(s), fixtures present
readback: 5 rows, sha256 decides, rewrap caught, blob id caught, LICENSE flagged
self-test: all checks passed
~~~

That is expected, not captured. The authoritative run is HivemindOS's, which writes its own result into `SELFTEST_OUTPUT.md` in the folder; I did not write that file and no line here claims a pass.

## Checks behind the expected pass

- `SAMPLE_HUB` index.md: `# Index` + header + `|---|---|---|`; rewrapped: same header with `|:--|:--|:--|` — 13 characters either way, so `len()` is unchanged by construction and the self-test asserts it rather than trusting the comment.
- `test_readback` also still requires 5 listing rows, an object id read for every row, a `LICENSE` row flagged on both the rule and the row count, and `verdict: PASS` on the clean sample.
- `test_clean`, `test_broken`, `test_folder` are untouched; they already ran before the failing check in the last run.

## Not confirmed

- The self-test itself: never executed by me here. Untested until the runner reports.
- The live path (`tree`, `verify` without `--offline`): still never executed from any step, and the Hub tree object-id field name is still unprobed. This change adds a guarded GitHub contents call to it.
- Nothing was uploaded, posted or published from this step.

## Left for the owner

Nothing to run by hand for correctness; HivemindOS's post-commit run supplies the real output. Separately, the publish play for this title is still unrun — five named paths only, `readback.py` and `self_test.py` edits ship with it.

[Cut off here: it ran out of room. Its next step can pick up from this point.]
