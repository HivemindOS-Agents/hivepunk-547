---
license: UNKNOWN
---

# agent-memory-lint-fixtures-index-v3

Dataset card for the third version of the agent-memory-lint fixture index.

## Files served

This folder ships exactly these five files, in this fixed order:

| # | File |
|---|------|
| 1 | `README.md` |
| 2 | `index.json` |
| 3 | `index.md` |
| 4 | `index_check.py` |
| 5 | `self_test.py` |

`.gitattributes` may also appear; it is the only tolerated extra.

## Index version

The version value read from this folder's own `index.json` is **`2`** (the `"version"` field). See `index.json` for the full record.

## Supersedes

This version replaces [agent-memory-lint-fixtures-index-v2](https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures-index-v2).

## License

`UNKNOWN` — this folder carries no license file. The owner should edit this README to set the correct license.

## Run it

```
python3 self_test.py
```

No arguments, no outside files, no network, standard library only. Expected exit code 0 and output:

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

## Provenance

Green self-test: HivemindOS runner run 43132441747, 2026-11-12 01:09 UTC, state `passed`. Source repository:
https://github.com/HivemindOS-Agents/hivepunk-547/tree/main/tools/agent-memory-lint-fixtures-index-v3
