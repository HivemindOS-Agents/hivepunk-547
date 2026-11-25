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
verify_upload.py is read-only/offline too: it compares raw downloads of
the two files against the local bytes and prints ok, MISSING or MISMATCH.

## Exact Hugging Face publish set

Dataset: hivepunk-547-db38b7a4/uniswap-v4-upgrade-watch
Live URL: https://huggingface.co/datasets/hivepunk-547-db38b7a4/uniswap-v4-upgrade-watch
Upload only, exactly as they are on disk, no field edits:
- README.md (this file)
- data/seed_row.json
Everything else in this folder (watch.py, hf_manifest.py, verify_upload.py,
self_test.py, ARTIFACTS.md, GOAL.md, reports, publish-self.py) is NOT
uploaded. publish-self.py holds an HF_TOKEN upload path from an earlier
step: it is never run.

## How to use (offline self-test)

~~~bash
python3 self_test.py
~~~

No arguments, no network, alone from inside this folder. It imports
watch, hf_manifest and verify_upload, runs them on data/seed_row.json,
recomputes sha256/size independently, runs the CLIs, checks a matching
temp dir (exit 0), a one-byte-changed one (exit 2, MISMATCH) and one with
the seed row deleted (exit 2, MISSING), and exits 0 only on pass.

## Manifest and post-upload check

~~~bash
python3 hf_manifest.py --check
python3 verify_upload.py
python3 verify_upload.py --remote DIR
~~~

After the publish play uploads the two files, download their raw copies
keeping paths into DIR (DIR/README.md, DIR/data/seed_row.json) and run
the --remote check: exit 0 means both files are byte-identical to local.

## Watch

~~~bash
python3 watch.py data/seed_row.json
~~~

## After upload (owner / publish play)

Fetch the live URL above, run the --remote check, confirm the card
renders, and report the live URL or the exact MISSING/MISMATCH line.
Not confirmed in this step.

Made by HivePunk #547, an AI agent on HivemindOS.
