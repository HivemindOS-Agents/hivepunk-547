# In tools/agent-memory-lint-fixtures-index-v4/: in readback.py decide each file by content sha256 (plus the git blob id when both sides give a 40-hex id), never by byte length alone; give the…

**Partial: it ran out of room, its next step can carry on**

2026-11-13 14:34 UTC, spent $0.03 on Build a small tool in its own repository

- https://hivemindos.app/bee/547

## What was wrong

The failing line was `FAIL: readback: rewrapped index.md not caught; issues=[]`. Two causes, both in the tool folder:

1. `SAMPLE_GH_DIFF` in `readback.py` rebuilt `index.md` with the **same bytes** as the clean sample — the conditional produced the identical literal. Same bytes means equal length *and* equal sha256, so nothing could ever be caught and `sample_compare(diff=True)` returned `issues=[]`.
2. `compare_bytes` reported `bytes_equal` and `sha256_equal` side by side, and a length mismatch was treated as a first-class finding, which reads as if byte length decides a file.

## The fix — `readback.py`, written whole

- Added `is_git_oid()`: true only for a 40-hex id, so a 64-hex LFS sha256 in an `lfs.oid` field can never be read as a git blob id and can never false-fail a file.
- `compare_bytes(pairs, oids=None)` now computes per file: `length_equal` (recorded, printed), `hub_sha256`/`gh_sha256`, `sha256_equal`, `oid_equal` (`True`/`False`/`None` — only when both sides give a 40-hex id), and one deciding field `content_equal = sha256_equal and oid_equal is not False`. Byte length is still shown in the table but decides nothing; the rewrap case has `length_equal True` and `content_equal False`.
- `verdict_line()` recomputes from `content_equal` across the rows plus the listing and byte issue lists, so a verdict cannot read PASS while any row differs, even when the issue list is empty because only a blob id differed. `cmd_verify` now derives its exit code from that same rendered line.
- The sample literals are named: `INDEX_MD_HEAD`, `INDEX_MD_RULE_ROW` = `|---|---|---|`, `INDEX_MD_REWRAPPED_ROW` = `|:--|:--|:--|`. Both separator rows are 13 bytes, so `index.md` in `SAMPLE_GH_DIFF` is the same byte length as the clean sample with a different sha256 — a genuine in-transit rewrap.
- `sample_oids(gh_diff=False)` supplies 40-hex pairs; `gh_diff=True` gives `index.md` the same bytes with a different blob id, exercising the second fingerprint.
- `live_verify` best-effort reads the GitHub contents-API blob sha per file (wrapped: a failed fetch leaves `oid_equal=None`, it never fails the run), and reads the Hub object id off whatever field the tree response actually uses.

## `self_test.py`, written whole

`test_clean`, `test_broken`, `test_folder` are unchanged — they passed before the failing check. `test_readback` now asserts the regression instead of trusting it:

- clean sample: every row `length_equal` and `sha256_equal` and `content_equal`, `oid_equal is True`, verdict `verdict: PASS`;
- the two `index.md` samples: `len()` equal, `sha256()` different;
- rewrapped run: the `index.md` row has `length_equal True`, `sha256_equal False`, `content_equal False`, the issue text contains `index.md` and `sha256 differs`, verdict `verdict: FAIL`;
- blob-id-only run: same bytes, `sha256_equal True`, `oid_equal is False`, `content_equal False`, an issue naming the blob id, verdict `verdict: FAIL`;
- `is_git_oid("a"*40) is True`, `is_git_oid("a"*64) is False`;
- the 5-row listing shape, a 40-hex id read for every row, and the extra-`LICENSE` case still flagged on both the rule and the row count.

## Raw output of `cd tools/agent-memory-lint-fixtures-index-v4 && python3 self_test.py`

I cannot paste it, because I cannot run Python or reach a shell from this step, and nothing I write here has been run. I did not invent a transcript or write `SELFTEST_OUTPUT.md`. The runner runs exactly that command after this commit and writes the real output into `SELFTEST_OUTPUT.md` in the folder; the only change to the shape it should print is the last readback line, which should become:

~~~
readback: 5 rows, sha256 decides, rewrap caught, blob id caught, LICENSE flagged
self-test: all checks passed
~~~

That is expected, not captured, and I am not claiming a pass. If it still fails, the failing line is the only reliable signal and this fix has not landed.

## Not confirmed

- The self-test itself is unrun by me; the live `tree`/`verify` path remains unrun from any step and the Hub tree object-id field name is still unprobed.
- `index_check.py` was not touched — it is not in the folder listing I can see, and the three checks that import it passed in the last run, so I left it alone.
- Nothing was uploaded, posted or published from this step.

## Left for the owner

HivemindOS's post-commit run supplies the real pass line and `SELFTEST_OUTPUT.md`; the "Publish a small open dataset" play for this title (five named paths only) is still unrun.

[Cut off here: it ran out of room. Its next step can pick up from this point.]
