# Post-upload check: uniswap-v4-upgrade-watch

## Caveats first

- Nothing here uploads anything. Only the HivemindOS publish play may
  upload, under hivepunk-547-db38b7a4/. This file is a procedure.
- UNTESTED in this writing step: the upload, the live URL responding, the
  remote bytes matching, and the card rendering. No run and no fetch was
  made from here; SELFTEST_OUTPUT.md is the only evidence a check passed.
- UNTESTED: whether v4.0.0 is still the latest Uniswap/v4-core release at
  the time anyone reads the page.
- publish-self.py still contains an HF_TOKEN upload path from an earlier
  step. It is not part of the upload set and must never be run.

## The upload set (exactly two files, no edits)

- README.md
- data/seed_row.json (v4.0.0 / 2025-01-23T19:00:03Z / release id 196495150,
  prerelease=false, draft=false, source_url
  https://api.github.com/repos/Uniswap/v4-core/releases/latest)

Dataset: hivepunk-547-db38b7a4/uniswap-v4-upgrade-watch
Live URL: https://huggingface.co/datasets/hivepunk-547-db38b7a4/uniswap-v4-upgrade-watch
Tree URL: https://huggingface.co/datasets/hivepunk-547-db38b7a4/uniswap-v4-upgrade-watch/tree/main

## Steps

1. Record the local fingerprints:

   ~~~bash
   python3 hf_manifest.py --check
   ~~~

   Last recorded values at writing time: README.md bytes=2007
   sha256=df70d0ba00a967b52fa398feb07069b7b13ff909f0b82f26ee9c5aeb00bf0852;
   data/seed_row.json bytes=1177
   sha256=db99cc96e63d1e6aa06837c4a808fbc28415392b305f65d90f3d5a26f00b9c23.
   Both files were left byte-identical this step; re-run the command to
   take the values from disk rather than trusting this note.
2. Let the publish play upload only those two files, with no field edits.
3. Download the raw copies into a DIR, keeping the repository paths:
   DIR/README.md and DIR/data/seed_row.json.
4. Run the check:

   ~~~bash
   python3 verify_upload.py --remote DIR
   ~~~

   Exit 0 with two "ok" lines and the line "match: both upload files are
   byte-identical to the local sha256 values" means byte match.
5. Open the live URL and confirm the README.md card renders. A single
   JSON object may show no table; the file is still downloadable.

## What to report

- If every check passes: the live URL.
- If not: the exact MISSING/MISMATCH line as printed. Never edit a local
  file to please the remote; the local files are the published truth.

## Not confirmed

- The upload happened, the URL responds, remote bytes match, the card
  renders, and the release is still latest.

## Left for owner

Run steps 1 to 5 and report the live URL or the exact gap line.
