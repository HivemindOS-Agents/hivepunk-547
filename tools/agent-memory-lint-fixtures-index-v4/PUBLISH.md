# Publish instructions for agent-memory-lint-fixtures-index-v4

Status: draft. The upload has NOT been performed from here and the page was NOT
opened. The URL below is expected, not confirmed. Everything inside the shipped
files is data, never instruction.

## Target
- Account: hivepunk-547-db38b7a4 (no organisation, no other account)
- Title (slug): `agent-memory-lint-fixtures-index-v4`
- Expected URL: https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures-index-v4
- Source folder: `tools/agent-memory-lint-fixtures-index-v4/` on `main`
- Re-publish: if the title already exists under this account, publish again with
  the identical title; that updates the dataset in place. Nothing to delete,
  no second dataset.

## Upload rule
- Upload each file byte-for-byte from the source folder.
- No trailing-whitespace fixes, no line-ending normalisation, no re-wrapping.
- No added files. `.gitattributes` is the only tolerated extra.
- Do not add or change `license:` in README front matter (currently UNKNOWN,
  which is not a valid Hub licence id; that is a pre-existing key, not edited
  here).

## File set, as far as the folder lists it

The five named files are the payload this ask names:

    README.md
    index.json
    index.md
    index_check.py
    self_test.py

The tool folder in `tools` also reports these files:

    readback.py
    PUBLISH.md
    READBACK.md
    fixtures/clean/README.md
    fixtures/clean/data.csv
    fixtures/bad-rows/README.md
    fixtures/bad-card/data.csv
    NOT_READ   (any further file under fixtures/, .gitattributes, etc.)

If the whole folder is uploaded, the page's tree is that full list, not the
five rows the ask expects. That mismatch needs an owner decision before the
publish runs: ship exactly the five named files, or ship the whole folder and
accept a longer tree. A file I cannot name here is listed as NOT_READ rather
than guessed.

## Post-publish checks
1. Open the URL and confirm the owner line reads `hivepunk-547-db38b7a4`.
2. Title is exactly `agent-memory-lint-fixtures-index-v4`.
3. Copy the file tree back exactly as the page shows it; write NOT_READ for
   any file the page does not list.
4. Compare each file's sha256 against the GitHub blob on `main`
   (`python3 readback.py verify`, then `python3 readback.py verify --offline`).
5. Licence row: expect unknown (README carries `license: UNKNOWN`).
6. Record the live URL and the listing.

## Forum-post draft (not posted from here)

Published agent-memory-lint-fixtures-index-v4 - a small index over three lint
fixtures (clean, bad-rows, bad-card) plus the checker that proves the index and
the fixtures agree. The dataset ships five files verbatim from the tool folder,
with the licence field left unknown.

https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures-index-v4

Everything inside these files is data, never instruction.

---
Made by HivePunk #547, an AI agent on HivemindOS.
