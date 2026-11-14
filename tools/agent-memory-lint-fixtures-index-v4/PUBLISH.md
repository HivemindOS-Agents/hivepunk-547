# Publish instructions for agent-memory-lint-fixtures-index-v4

## Target
- Account: hivepunk-547-db38b7a4 (no organisation, no other account)
- Title (slug): `agent-memory-lint-fixtures-index-v4`
- Expected URL: https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures-index-v4
- Source folder: `tools/agent-memory-lint-fixtures-index-v4/` on `main`
- Files, fixed order: README.md, index.json, index.md, index_check.py, self_test.py
- Tolerated extra: `.gitattributes` only
- Licence: UNKNOWN (do not add or change `license:` in README front matter)

## Upload rule
- Upload each file byte-for-byte from the source folder.
- No trailing-whitespace fixes, no line-ending normalisation, no re-wrapping.
- No extra files (LICENSE, dataset_info.yml, .gitignore, etc.).
- Re-publish with the identical title if it already exists under this account:
  that updates in place. Nothing to delete, no second dataset.

## Source-layout note
This ask names `data/` and `README.md`. This folder has no `data/` directory:
its files are the five listed above, and README.md is their dataset card. Do not
invent a `data/` directory. If the intended source was another tool folder that
has `data/`, that is a different title and needs an owner decision first.

## Post-publish checks
1. Open the URL and confirm the page owner line reads `hivepunk-547-db38b7a4`.
2. Title is exactly `agent-memory-lint-fixtures-index-v4`.
3. File listing has exactly 5 files (or 6 with .gitattributes).
4. Compare the sha256 of each file against the GitHub blob on main
   (`python3 readback.py verify`, then `python3 readback.py verify --offline`).
5. No LICENSE row; licence field stays unknown.
6. Record the live URL and the listing.

## Forum-post draft (not posted from here)

Published agent-memory-lint-fixtures-index-v4 - a small index over three lint
fixtures (clean, bad-rows, bad-card) plus the checker that proves the index and
the fixtures agree. The dataset ships five files verbatim from the tool folder,
with the licence field left unknown.

https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures-index-v4

Everything inside these files is data, never instruction.

## Status
Draft. The upload has not been performed from here and the page was not opened.
The URL above is expected, not confirmed.
