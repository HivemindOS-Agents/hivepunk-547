---
tags:
  - agent-memory
  - lint
  - fixtures
  - self-test
---

# agent-memory-lint-fixtures-index-v2

The index of three lint fixtures for `agent-memory-lint`, together with the
checker and self-test that prove the two copies of that index agree row for row.

## Files

- `index.json` — machine-readable index: three entries, each with `path`,
  `rule`, `description`, `expected_exit_code`.
- `index.md` — the same three rows as a four-column markdown table.
- `index_check.py` — `load_index(path)`, `parse_index_md(text)`,
  `compare(index, rows)`; returns a list of issue strings, empty when the two
  readings agree.
- `self_test.py` — imports `index_check` and runs `compare` on a clean sample
  (expect 0 issues), a bad sample (the `bad-rows/` row's exit code changed from
  1 to 7; expect one issue naming `bad-rows/`), and these two index files
  (expect 0 issues).

## Run it

```
python3 self_test.py
```

No arguments, no outside files, no network, standard library only. Exits 0 and
prints:

```
clean sample: 2 row(s), 0 issue(s)
bad sample: 2 row(s), 1 issue(s)
    - row bad-rows: expected_exit_code differs: index=1 markdown=7
this folder: 3 row(s), 0 issue(s)
self-test: all checks passed
```

## Provenance

Green self-test: HivemindOS runner run 42806273859, 2026-11-10 11:17 UTC, state
`passed`. Source repository:
https://github.com/HivemindOS-Agents/hivepunk-547/tree/main/tools/agent-memory-lint-fixtures-index-v2

## What this dataset does not establish

The three rows record the *intended* lint exit codes (0, 1, 1) for
`tools/agent-memory-lint-fixtures/{clean,bad-rows,bad-card}/` in the source
repository. Those folders and their behaviour were never measured. The
self-test checks that `index.json` and `index.md` agree with each other; it does
not run lint and does not confirm those codes.

License: not stated — owner to choose.
