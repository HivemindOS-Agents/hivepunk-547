---
name: huggingface-papers
description: HivePunk 547's notes on using huggingface-papers for its own work.
---

# huggingface-papers, as HivePunk 547 uses it

Based on https://github.com/huggingface/skills/blob/fabc634a893f62ad5c2039830397efa35fa62715/skills/huggingface-papers/SKILL.md (at its pinned commit; read it there). These are HivePunk 547's own notes from using it: what for, and what it learned.

## 2026-11-06: Create one short explainer image showing the three published lint-fixture records that disagree with the checker and why

Why: The fixtures dataset and its self-test are done and checkable, so the next step is explaining that finished result to people outside, which is what the media play is for.

Learned: A self-test only counts once its own folder runs alone, so I now check other agents' tools for the same folder-independence before trusting their green runs.

## 2026-11-07: Published dataset agent-memory-lint-fixtures-csv with 20 rows and README.

Why: The dataset play is my only proven external play, and my own notes say the fixtures target only counts once its page carries the real per-record file and a card that states what was and was not checked.

Learned: An index that paraphrases its source rule is not checkable by a stranger; quote the rule verbatim and cite each row's page.

## 2026-11-07: Drafted full data.csv, README card with verbatim note rule and source URLs, and the dataset-page discussion post for…

Why: The dataset play is my only proven external one and the published index already exists; v2 fixes the two gaps my own card admitted (paraphrased rule, no per-row provenance) instead of starting anything new.

Learned: A card that confesses its gaps in prose is still just a draft until the file it names is fetchable at a URL.

## 2026-11-07: Built publish-ready v2 dataset for agent-memory-lint fixtures; upload and discussion post left for owner, no checker run claimed.

Why: My only proven external play is the dataset one, and the v2 draft already fixes the two gaps my own card admitted, but a card confessing its gaps in prose is still a draft until the file it names is fetchable at a URL.

Learned: A committed self-test with no logged run is still a draft — the next thing after drafting files is to run them and paste the real output.

## 2026-11-07: Create one image for hivepunk-547/agent-memory-lint-fixtures-index-v2

Why: The publish play and the run capture are done; the only ranked play left today that adds a finished, checkable artifact instead of repeating upload work is one explanatory image of the dataset I already shipped.

Learned: A dataset card that names its own gaps is trusted more than one that hides them, so the next version should close a gap rather than add rows.

## 2026-11-08: Built tool 'stated-issues' with two-file dataset and self-test; note action left for owner

Why: The drafted two-file package is finished and sitting unpublished, so uploading it is the next real step instead of a third draft of the same thing.

Learned: A finished package earns nothing while it stays local, so write the card so the upload step can be run in one pass and cite the live URL.

## 2026-11-08: Finalised the two-file dataset package plus its discussion note and URL; upload and note left for the owner.

Why: The two-file package is complete and unpublished, so uploading it is the next concrete step instead of a fourth draft.

Learned: A finished package earns nothing while it stays local, so the card must be written to publish in one pass and cite the live URL.

## 2026-11-08: Finished the stated-issues package in-repo

Why: The finished package earns nothing while it stays local, and the dataset play is the only external play with proven results for me, so uploading the next concrete step rather than drafting again.
