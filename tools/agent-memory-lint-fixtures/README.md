---
license: cc0-1.0
task_categories:
- text-classification
language:
- en
tags:
- agent-memory
- fixtures
- lint
- label-discipline
---

# agent-memory-lint-fixtures

Six small memory-record fixtures for one rule: **a record whose hand-written labels disagree with the labels computed from its own fields must carry a note; a record that agrees must not.** This is a companion fixture set for the checker `lint_records.py` in the repository folder `tools/agent-memory-lint-fixtures`. The checker is not included here, because this dataset is exactly two files.

## Files

- `sample_records.jsonl` — six records, ids `L004`, `L005`, `L012`, `L013`, `L018`, `L020`, in that order. One JSON object per line.
- `README.md` — this card.

## Record fields

| field | meaning |
|---|---|
| `id` | fixture id, `L0nn` |
| `body` | the record's text; whitespace-only counts as empty |
| `source` | the source string; blank counts as unsourced |
| `source_date` | `YYYY-MM-DD`, compared against the fixed reference date `2026-11-01` |
| `expected_labels` | hand-written labels: `body` (nonempty/empty), `origin` (sourced/unsourced), `date` (fresh/stale) |
| `note` | present only when the hand labels disagree with the computed labels; names the computed labels and the rule branch that fires |

## The rule

For each record, compute three labels from the record's own fields:

- `body` = `empty` if the body is blank or whitespace-only, else `nonempty`
- `origin` = `unsourced` if the source string is blank, else `sourced`
- `date` = `stale` if `source_date` is more than 365 days before `2026-11-01`, else `fresh`

If the computed labels differ from `expected_labels`, the record MUST carry a `note`. If they match, the record MUST NOT carry a `note`.

## The six rows

| id | hand labels vs computed | note |
|---|---|---|
| L004 | disagrees (body) | added — whitespace-only body |
| L005 | disagrees (origin) | added — blank source |
| L012 | disagrees (body, date) | added — whitespace-only body; source date 2026-07-20 is 104 days before the reference date, so fresh, not stale |
| L013 | disagrees (date) | added — source date 2024-11-01 is 730 days before the reference date, so stale |
| L018 | agrees | none |
| L020 | agrees | none — 331 days before the reference date, so fresh (near-boundary case) |

## Intended use

Checking a memory-lint rule against a handful of hand-labelled rows, including two near-boundary cases (L020 at 331 days, L012 at 104 days) and one clearly stale date (L013 at 730 days). Small enough to read in one sitting; not a benchmark and not a training set.

## Provenance and limits

- Derived from the fixture folder `tools/agent-memory-lint-fixtures` in the `HivemindOS-Agents/hivepunk-547` repository. Only these two files are published here.
- No keys, credentials, personal details or private values appear in any record; all bodies and sources are invented.
- The checker that consumes this format is not part of this dataset, and no run result for it is asserted here. Nothing in this card claims the fixture set has been run or has passed anywhere.
- `source_date` values are fixed strings, and the 365-day boundary is measured against the hard-coded reference date `2026-11-01`, not against today.

## License

CC0-1.0 (public domain dedication).
