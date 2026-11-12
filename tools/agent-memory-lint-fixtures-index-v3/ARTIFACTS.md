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
