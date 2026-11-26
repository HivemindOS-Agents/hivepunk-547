# uniswap-v4-upgrade-watch

## Caveats first

- Verified seed row: Uniswap/v4-core v4.0.0 / 2025-01-23T19:00:03Z,
  release id 196495150, prerelease=false, draft=false, from
  https://api.github.com/repos/Uniswap/v4-core/releases/latest
- UNTESTED: Whether v4.0.0 is still latest at view time.
- UNTESTED: HF upload, remote byte match, and card rendering. This step
  does not upload anything; the publish play does that.
- UNTESTED: HF viewer may show no table for a single JSON object.
  The file is downloadable regardless.
- A person decides; an agent never merges or publishes.

## What this is

watch.py reads data/seed_row.json offline and prints the verified line.
hf_manifest.py is read-only/offline: it validates that seed through
watch.load_seed and fingerprints the exact two-file publish set.

## Exact Hugging Face publish set

Dataset: hivepunk-547-db38b7a4/uniswap-v4-upgrade-watch
Live URL: https://huggingface.co/datasets/hivepunk-547-db38b7a4/uniswap-v4-upgrade-watch
Upload only, exactly as they are on disk, no field edits:
- README.md (this file)
- data/seed_row.json
Everything else in this folder (watch.py, hf_manifest.py, self_test.py,
ARTIFACTS.md, GOAL.md, reports, publish-self.py) is NOT uploaded.

## How to use (offline self-test)

~~~bash
python3 self_test.py
~~~

No arguments, no network, alone from inside this folder. It imports
watch and hf_manifest, runs them on data/seed_row.json, recomputes
sha256/size independently, runs both CLIs, and exits 0 only on pass.

## Manifest

~~~bash
python3 hf_manifest.py --check
python3 hf_manifest.py
~~~

First prints a short checklist, second prints JSON with bytes/sha256.

## Watch

~~~bash
python3 watch.py data/seed_row.json
~~~

## After upload (owner / publish play)

Fetch the live URL above, confirm README.md and data/seed_row.json
match the sha256 in hf_manifest output, and confirm the card renders.
Report the live URL or the exact gap. Not confirmed in this step.

Made by HivePunk #547, an AI agent on HivemindOS.
