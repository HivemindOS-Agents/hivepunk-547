# agent-memory-viewer-readback-log

opportunity: opp-547-46

## Caveats first

- Labels are hand-derived from research notes dated 2026-11-22, not source-verified by re-fetch in this writing step.
- UNKNOWN rows list claims/source licences not verified from what was read.
- Could not confirm: live Hugging Face listing status, live source pages re-fetch, and self-test exit 0.
- Intended (NOT confirmed) dataset URL: https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-research-rows
- Do not touch tools/agent-memory-lint-fixtures/ for this work.

## What this is

Sourced research rows about rohitg00/agentmemory for an agent-memory viewer/readback log. One row per claim in rows.csv.

Columns: row_id,subject,claim,label,source_url,observed_date
Labels: FACT (source states it), DERIVED (follows from source), UNKNOWN (not verifiable from what was read).

## How to use

~~~bash
python3 agent_memory_rows.py --check rows.csv
python3 self_test.py
~~~

Run self_test.py with no arguments, no network, alone from this folder. agent_memory_rows.py validates rows.csv (allowed sources, labels, dates, unique ids) and exits 0 only when valid.

## Untested parts (marked untested)

- UNTESTED: source pages were not re-fetched in this writing step; individual FACT claims may no longer be on their pages.
- UNTESTED: no live Hugging Face dataset was published or confirmed; URL above is intended only.
- UNTESTED: self-test exit 0 was not confirmed from this writing step; HivemindOS runner result in SELFTEST_OUTPUT.md is authoritative.
- Licence of agentmemory sources: UNKNOWN (licence text not read).

## ARTIFACTS.md log (merged into README due to 4-file limit)

- Artifact: rows.csv - 14 rows (FACT 6, DERIVED 4, UNKNOWN 4), sources listed in agent_memory_rows.py ALLOWED.
- Artifact: agent_memory_rows.py - validator/CLI for rows.csv.
- Artifact: self_test.py - standalone test importing agent_memory_rows on rows.csv plus bad-row cases and CLI temp copies.
- Artifact: README.md (this file) - usage, caveats, untested marks, and this ARTIFACTS log. Owner may split this section verbatim into ARTIFACTS.md.
- Command: python3 self_test.py (no args, no network, alone from this folder).
- Raw output slot: paste runner SELFTEST_OUTPUT.md here when produced; nothing here is a run log.
- Left for owner: let runner run self_test.py, then separate publish step if wanted, then confirm live URL and replace intended URL.

Made by HivePunk #547, an AI agent on HivemindOS. A person decides; an agent never merges or publishes.
