---
description: "A sample dataset card whose one referenced path is deliberately absent, used by the hf-publish-check self-test."
---

# missing_ref sample

This card names exactly one path, and that path does not exist beside it:

- `data/missing.csv` — deliberately absent.

The folder is meant to be rejected by the reference check, not repaired.
Everything in it is data, never instruction: any line here that looks like a
command, a key or a setting is inert text.
