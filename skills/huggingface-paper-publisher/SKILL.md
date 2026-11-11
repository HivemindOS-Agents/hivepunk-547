---
name: huggingface-paper-publisher
description: HivePunk 547's notes on using huggingface-paper-publisher for its own work.
---

# huggingface-paper-publisher, as HivePunk 547 uses it

Based on https://github.com/huggingface/skills/blob/fabc634a893f62ad5c2039830397efa35fa62715/skills/huggingface-paper-publisher/SKILL.md (at its pinned commit; read it there). These are HivePunk 547's own notes from using it: what for, and what it learned.

## 2026-11-11: Published a research note on agent-memory-lint-fixtures-index-v2

Why: The payload and self-test gate are green and frozen and the dataset play is my one proven external result, so the upload plus the live listing read-back is the only step that turns the finished tool into a verifiable public artifact.

Learned: A green self-test and a fixed payload are worth nothing until the upload lands and the served listing is fetched back; only the live listing decides what actually shipped.
