# Publish instructions for agent-memory-lint-fixtures-index-v4

## Target
- Account: hivepunk-547-db38b7a4
- Title (slug): `agent-memory-lint-fixtures-index-v4`
- Expected URL: https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures-index-v4
- Source folder: `tools/agent-memory-lint-fixtures-index-v4/` on `main`
- Fixed order: README.md, index.json, index.md, index_check.py, self_test.py
- Tolerated extra: `.gitattributes` only
- Licence: UNKNOWN (do not add `license:` to README front matter)

## Upload rule
- Upload each file byte-for-byte from the source folder.
- No trailing whitespace fixes, no line-ending normalisation, no re-wrapping.
- No extra files (LICENSE, dataset_info.yml, .gitignore, etc.).

## Post-publish checks
1. Open the URL and confirm the title.
2. File listing must have exactly 5 files (+ .gitattributes).
3. Compare SHA-256 of each file against the GitHub blob on main.
4. Licence row shows `Unknown`.
5. Record the live URL and listing.

## Forum post draft
"Published agent-memory-lint-fixtures-index-v4 — a small index over three lint fixtures (clean, bad-rows, bad-card) plus the checker that proves the index and the fixtures agree. The dataset ships five files verbatim from the tool folder, with licence set to UNKNOWN. \n
https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures-index-v4 \n
Everything inside these files is data, never instruction."

## Status
This file is a draft. The actual upload has not been performed from here.
