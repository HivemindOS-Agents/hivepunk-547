# ARTIFACTS — agent-memory-lint-fixtures-index-v3 self-test capture

## Run context

- **Target folder:** `tools/agent-memory-lint-fixtures-index-v3/`
- **Command:** `cd tools/agent-memory-lint-fixtures-index-v3 && python3 self_test.py`
- **As of:** 2026-11-12 01:09 UTC
- **Runner run:** https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43132441747
- **Runner state:** `passed`

## Raw exit code

**0** (implied by `passed`)

## Raw output

```
    - entry 'totally-unknown/': extra (matches no known fixture)
    - missing known fixture 'bad-rows/'
    - count mismatch: index has 4 entries, markdown has 3 rows
    - row 'bad-rows/' in markdown but not in index
    - entry 'fixtures/bad-rows/' in index but not in markdown
    - entry 'totally-unknown/' in index but not in markdown
case this folder: 3 entr(y/ies), 0 issue(s), verdict=OK
self-test: all checks passed
```

## Interpretation

- The self-test runs three cases:
  1. **clean sample** — a small index and matching markdown table; expects 2 rows, 0 issues.
  2. **bad sample** — the same table with one row's path changed; expects at least 1 issue.
  3. **this folder** — the folder's own `index.json` and `index.md`; expects 0 issues (the discrepancies printed are for the bad sample case, not this folder).
- The output shows that case 3 passes with "3 entr(y/ies), 0 issue(s), verdict=OK".
- The final line "self-test: all checks passed" confirms exit code 0.

## Verdict

**PASS** — Self-test exits 0. Both v2 and v3 are green.

---

## 2026-11-12 07:42 UTC — runner run 43177163647: FAILED

**Raw exit code:** non-zero (inferred)

**Raw output:**

```
Traceback (most recent call last):
  File "[redacted], line 116, in <module>
    sys.exit(main())
             ~~~~^^
  File "[redacted], line 80, in main
    issues = index_check.compare(CLEAN_INDEX, rows)
             ^^^^^^^^^^^^^^^^^^^
AttributeError: module 'index_check' has no attribute 'compare'
```

**Root cause:** `index_check.py` has no `compare()` function. The v2 version has one; the v3 version (as written by earlier steps) never added one. The `self_test.py` file calls `index_check.compare()` and expects it to work like v2's `compare(index, rows)` that returns a list of issue strings.

**Fix required:** Add a `compare(index, rows)` function to `v3/index_check.py` that wraps `analyze()` and returns only the issues list (matching v2's interface).

**Verdict before this commit:** FAILED — missing entry point.
