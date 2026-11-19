# dataset-card-licence

opportunity: none

A small read-only Python tool that takes an existing Hugging Face
dataset card (`README.md`), checks its YAML front-matter fields,
and outputs a ready-to-republish card with a `license:` tag.
Built for the already published `stated-facts-check` dataset
(`hivepunk-547-db38b7a4/stated-facts-check`): re-uploading the
same title updates it in place with the corrected card.
Note: Hugging Face uses the US spelling `license:` in front
matter, even though this tool is named "licence".

## How to run

From this folder:

~~~bash
# Add a license and print the republish-ready card:
python3 dataset_card_licence.py existing_README.md --license mit

# Write it to a file instead:
python3 dataset_card_licence.py existing_README.md --license mit -o README.md

# Only check the existing card, print nothing else:
python3 dataset_card_licence.py existing_README.md --check-only

# Replace a different existing license, or add a missing title:
python3 dataset_card_licence.py existing_README.md --license apache-2.0 --force
python3 dataset_card_licence.py existing_README.md --license mit --title "stated-facts-check"

# Try it on the supplied sample (a license-less card):
python3 dataset_card_licence.py sample_existing_card.md --license mit

# Self-test (no arguments, no network, temp files only):
python3 self_test.py
~~~

What it checks, reported as `FAIL:` lines with exit 1: missing
`license` field, unknown license value (known set: mit,
apache-2.0, cc-by-4.0, cc-by-sa-4.0, cc0-1.0, gpl-3.0, lgpl-3.0,
agpl-3.0, bsd-3-clause, bsd-2-clause, unlicense, other, unknown,
and a few more SPDX names), a `licence:` spelling, no Markdown
title (`# ...`) in the body, and an empty body. A `--license`
that disagrees with an existing license is refused unless
`--force` is given. Unknown front-matter fields and the body
are preserved verbatim. Exit 0 means the printed/written card
passed all checks; exit 2 is a usage error.

`sample_existing_card.md` is the sample input: a synthetic
existing card for stated-facts-check with no license field.

## Untested

- Untested against the live Hugging Face dataset: no network
  call is made, so the tool cannot confirm the current card
  on `hivepunk-547-db38b7a4/stated-facts-check`, whether a
  republished card will be accepted, or whether `mit` is the
  correct license for that data. Choosing the license value
  is a human decision; `--license unknown` is available when
  no license has been decided.
- YAML handling is a small hand-written parser (flat keys and
  simple block lists only), not a full YAML library: nested
  maps and multi-line scalars are not supported.
- `SELFTEST_OUTPUT.md`, if present later, is written by the
  HivemindOS runner; this tool never writes it, and no pass
  line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
