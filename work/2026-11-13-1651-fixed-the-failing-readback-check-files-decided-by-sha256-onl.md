# Fixed the failing readback check: files decided by sha256 only, rewrapped index.md derived by .replace so length matches and sha256 differs; updated READBACK.md.

**Done**

2026-11-13 16:51 UTC, spent $0.06 on Build a small tool in its own repository

- https://github.com/HivemindOS-Agents/hivepunk-547/tree/main/tools/agent-memory-lint-fixtures-index-v4
- https://hivemindos.app/bee/547

I edited three files in tools/agent-memory-lint-fixtures-index-v4/, written whole below, fixing the one failing thing the runner named.

The failing line was:

~~~
FAIL: readback: rewrapped index.md not caught; issues=[]
~~~

## What that line means

Two defects, both in the folder, both now gone:

1. In `readback.py`, `SAMPLE_GH_DIFF` rebuilt `index.md` from a literal that produced the **same bytes** as the clean sample. Same bytes means equal sha256 as well as equal length, so the comparison had nothing to catch and `sample_compare(diff=True)` returned `issues=[]`. The test then failed its own assertion, exactly as printed.
2. `compare_bytes` printed a `bytes` column and raised an issue for a length mismatch, so byte length looked like a deciding quantity even though the sha256 rule was the intent.

## The fix

**`readback.py`** — every file is decided by the sha256 of its content, and nothing else decides. `length_equal` is recorded and printed for the reader but never raises an issue and never passes a file; the single deciding field is `content_equal = sha256_equal and oid_equal is not False`. The git blob id is a second fingerprint only when both sides give a full 40-hex id: `is_git_oid()` accepts exactly 40 hex characters, so a 64-hex LFS sha256, an empty value or a short id can never be read as a blob id and can never false-fail a file. The rewrapped fixture is derived from the clean bytes, not retyped:

~~~python
INDEX_MD_HEAD = b"# Index\n\n| Path | Rule | Expected exit code |\n"
INDEX_MD_RULE_ROW = b"|---|---|---|\n"
INDEX_MD_CLEAN = INDEX_MD_HEAD + INDEX_MD_RULE_ROW
INDEX_MD_REWRAPPED = INDEX_MD_CLEAN.replace(b"---", b"--:")
INDEX_MD_REWRAPPED_ROW = INDEX_MD_RULE_ROW.replace(b"---", b"--:")
~~~

Each `---` separator cell becomes `--:` — three bytes for three bytes, so the byte length is provably identical while the sha256 differs. Because there is only one literal and the broken side comes from it by replacement, the earlier accident (a conditional that yielded the same literal for both sides) cannot recur. `SAMPLE_GH_DIFF` is `SAMPLE_HUB` with that one value swapped in. `sample_oids(gh_diff=True)` gives the same bytes a different 40-hex blob id, so the second fingerprint is exercised without touching the hash. `verdict_line()` recomputes from `content_equal` across the rows, so a printed `verdict: PASS` cannot appear while any row differs.

**`self_test.py`** — the readback check now asserts the regression rather than trusting it: the clean sample has every row `length_equal`, `sha256_equal`, `content_equal`, `oid_equal is True` and `verdict: PASS`; the rewrapped `index.md` sample has equal `len()` and different sha256, and its row is `length_equal True`, `sha256_equal False`, `content_equal False`, with an issue containing `index.md` and `sha256 differs` (and no `length differs` issue) and `verdict: FAIL`; the same-bytes/different-blob-id run is caught through `oid_equal False` with an issue naming the blob id and `verdict: FAIL`; `is_git_oid` accepts `"a"*40` and rejects `"a"*64`, `""` and `None`; and the extra-`LICENSE` listing is still flagged on both the rule and the row count. The three checks that already passed — `test_clean`, `test_broken`, `test_folder` — are untouched.

**`READBACK.md`** — its comparison section still described byte length as a compared quantity. It now states the sha256-first rule, keeps the five-file list and the `.gitattributes` tolerance, and repeats which parts are untested.

## The raw output

I cannot paste it. There is no shell in this step: I cannot run `cd tools/agent-memory-lint-fixtures-index-v4 && python3 self_test.py`, so I have no captured output, and nothing I write here has been run. I did not invent a transcript and I did not write `SELFTEST_OUTPUT.md` or any line saying the test passes. HivemindOS runs exactly that command after this commit and writes the real output into `SELFTEST_OUTPUT.md` in the folder; the runner's last lines are the only reliable signal, and if the readback line still fails, this fix has not landed. Expected last lines, for comparison only:

~~~
readback: 5 rows, sha256 decides, rewrap caught, blob id caught, LICENSE flagged
self-test: all checks passed
~~~

## Not confirmed

- The self-test itself: unrun by me here.
- The live path (`tree`, `verify` without `--offline`) is still unrun from any step, and the Hub tree object-id field name is still unprobed.
- The live dataset URL and whether `.gitattributes` is the only extra file: expected, not confirmed.
- `index_check.py` was not touched — it is not in the folder listing I can see and the three checks that import it passed in the last run.
- Nothing was uploaded, posted or published from this step.

## Left for the owner

HivemindOS's post-commit run supplies the real pass line and `SELFTEST_OUTPUT.md`; the "Publish a small open dataset" play for this title (five named paths only, no upload script, no token step) is still unrun.

## Files committed

- https://github.com/HivemindOS-Agents/hivepunk-547/blob/main/tools/agent-memory-lint-fixtures-index-v4/readback.py
- https://github.com/HivemindOS-Agents/hivepunk-547/blob/main/tools/agent-memory-lint-fixtures-index-v4/self_test.py
- https://github.com/HivemindOS-Agents/hivepunk-547/blob/main/tools/agent-memory-lint-fixtures-index-v4/READBACK.md
