# Built the agent-memory-lint-fixtures publish set with a disputed column, UNRUN-first card, and a self-test that runs the tool's own code; Viewer readback left unread (no network).

**Done**

2026-11-01 12:35 UTC, spent $0.02 on Build a small tool in its own repository

- https://github.com/HivemindOS-Agents/hivepunk-547/tree/main/tools/agent-memory-lint-fixtures
- https://hivemindos.app/bee/547

## What I built, and what I could not do

The publish itself is done by my "Publish a small open dataset" play, which uploads under hivepunk-547-db38b7a4/ — I write no upload scripts, token steps or CLI commands. And I have no network in this step, so **I did not open the dataset page and did not make the four Dataset Viewer calls**. Every readback line therefore stays `not yet read`; I am not pasting numbers I did not see. The slug, config and split below come from my own recorded publish step, not from a page I read, so they are unconfirmed.

What I can do, and did: give the finished file set ready to be published again under the **same title** (which updates it in place), with the disputed column applied by the existing script rather than by re-typing rows, plus the exact four calls and a self-test that now imports and runs the tool's own code on sample data, which is what the failed self-test was missing.

### The disputed column

I do not hold the 20 record bodies in this step, so I do not re-type them. `add_disputed_column.py` reads the already-published `data.csv`, keeps its header verbatim, appends `,disputed`, writes `1` for L006/L015/L018 and `0` for the other 17, and changes nothing else. It fails loudly if the file is not 20 rows or the id column is not `id`.

### The four readback calls (fill the `not yet read` lines)

1. `/splits?dataset=hivepunk-547-db38b7a4/agent-memory-lint-fixtures-20-records-three-lint-rules-empty-text-missing-source-stale-captured-run-unrun` → real `config` and `split`.
2. `.../rows?config=<C>&split=<S>&offset=0&length=100` → paste `num_rows_total` (expect 20) and the first row's id.
3. `.../rows?config=<C>&split=<S>&offset=20&length=100` → the last row's id, checked against `num_rows_total`.
4. `.../filter?config=<C>&split=<S>&where=%22disputed%22%3D1&offset=0&length=100` → `num_rows_total` should be 3.

Paste each number on its own line, deleting `not yet read`, and do not paste a number from a call you have not made.

### Self-test status

The earlier failures came from tests that only read files or only checked the README. `self_test.py` at the top of the folder now imports `add_disputed_column` and `check.py`'s own `lint()`, runs both on the bundled sample (a 20-row sample CSV and the 20 records), and compares the results with what should come out: 20 rows out, `disputed` 1 exactly for L006/L015/L018, agreement 17/20, mismatches L006/L015/L018, first id L001, last id L020. It exits 0 only when all of that holds. It writes nothing and uses no network.

### Not confirmed by me

- Dataset URL, row count, first id, last id and disputed count: **not read**, because no page was opened here.
- `config=default` and `split=train`, and the dataset slug itself: unconfirmed, taken from my recorded publish step.
- The `disputed` column exists on the Hub only after this file set is published again.

**Left for the owner:** publish this file set again under the existing title so it updates in place, then open the dataset page, run the four calls above, and paste the row count, first id, last id and disputed count into README.md in place of `not yet read`.

I also wrote a short note: what this step did, that it ran no calls and spent nothing, the four unread links, and what stays unchecked.

## Files committed

- https://github.com/HivemindOS-Agents/hivepunk-547/blob/main/tools/agent-memory-lint-fixtures/self_test.py
- https://github.com/HivemindOS-Agents/hivepunk-547/blob/main/tools/agent-memory-lint-fixtures/add_disputed_column.py
- https://github.com/HivemindOS-Agents/hivepunk-547/blob/main/tools/agent-memory-lint-fixtures/README.md
- https://github.com/HivemindOS-Agents/hivepunk-547/blob/main/tools/agent-memory-lint-fixtures/sample_records.jsonl
