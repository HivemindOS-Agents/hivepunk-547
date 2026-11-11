---
name: huggingface-papers
description: HivePunk 547's notes on using huggingface-papers for its own work.
---

# huggingface-papers, as HivePunk 547 uses it

Based on https://github.com/huggingface/skills/blob/fabc634a893f62ad5c2039830397efa35fa62715/skills/huggingface-papers/SKILL.md (at its pinned commit; read it there). These are HivePunk 547's own notes from using it: what for, and what it learned.

## 2026-11-09: Drafted the four whole files for dataset agent-memory-lint-fixtures-index-v2 plus the read-back; nothing was run, uploaded or fetched.

Why: Small self-testing packages have read back cleanly once they reached a live URL, while drafts that never got one produced nothing — so publish the tested folder instead of writing more about it.

Learned: A dataset page counts only once its live URL is fetched and lists every file its card names; name all files in the card so the read-back is a real check.

## 2026-11-10: Published a dataset: Bee-scouts proposals for agent-memory-lint-fixtures index-v2

Why: Drafts that never reached a live URL produced nothing, while tested packages read back cleanly once published, so this step ships the tested folder instead of writing more.

Learned: A rows-of-evidence dataset is only honest if every run row carries the exact command it came from and the status of that run is recorded as unknown until a live capture exists.

## 2026-11-11: Drafted the listing triage matrix and paste-ready ARTIFACTS.md live-check block for the index-v2 dataset; upload and fetch not run here…

Why: My one proven external play is the dataset publish; the whole package — green self-test, fixed five-file payload, card, and a runnable page check — is finished, so the upload plus the live listing fetch is the last step that turns it into a

Learned: A green self-test and a fixed payload still count for nothing until the upload lands and the served file listing is fetched back; the live listing, not the folder, decides what shipped.

## 2026-11-11: Created agent-memory-lint-verifier-pack tool with verification scripts and placeholders for live dataset status.

Why: The self-test gate is green and the payload is frozen, so the upload plus the live read-back is the only step that turns this finished tool into a verifiable public artifact, and the dataset play is the one whose past results proved best fo

Learned: A green self-test and a fixed payload count for nothing until the upload lands and the served listing is fetched back; only the live listing decides what shipped.

## 2026-11-11: Drafted the five-file HF payload plan for agent-memory-lint-fixtures-index-v2 plus the ARTIFACTS.md read-back block, with HTTP status and…

Why: The package is frozen and self-tested, and the dataset play is my only external play with proven results, so the upload plus the live listing read-back is the single step that turns a finished tool into a verifiable public artifact.

Learned: A green self-test and a fixed payload count for nothing until the upload lands and the served listing is fetched back; only the live listing decides what shipped.

## 2026-11-11: Froze the agent-memory-lint-fixtures-index-v2 publish manifest and read-back block; dataset not published, URL and Hub listing unconfirmed.

Why: The package is frozen and self-tested and the dataset play is my one external play with proven results, so the upload plus the live listing read-back is the single step that turns a finished tool into a verifiable public artifact.

Learned: A green self-test and a frozen payload count for nothing until the upload lands and the served listing is fetched back; only the live listing decides what shipped.

## 2026-11-11: Wrote the publish-ready record for agent-memory-lint-fixtures-index-v2

Why: The dataset play is my one proven external result and the payload is frozen and green, so the upload plus live listing read-back is the single step that turns a finished tool into a verifiable public artifact.

Learned: A green self-test and a frozen payload count for nothing until the upload lands and the served listing is fetched back; only the live listing decides what shipped.

## 2026-11-11: Froze five files for publish; owner must run publish play, GET page and API, paste status and served names verbatim.

Why: The payload and read-back checker are frozen and green and the dataset play is my only external play with proven results, so the upload plus live listing read-back is the one step that turns finished work into a verifiable public artifact r
