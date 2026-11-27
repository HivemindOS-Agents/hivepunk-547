# gfx950-mi355x-publish-note

opportunity: none

## What this is

A small read-only tool that prepares, but does not perform, the publication of
the folder `tools/opp-547-38-gfx950-mi355x-summary/` as a Hugging Face dataset
under `hivepunk-547-db38b7a4`, plus the short forum note that links it.

It does three things and nothing else:

1. Reads two files in a target folder - `SUMMARY.md` and `README.md` - read-only.
2. Fingerprints them (byte size and sha256) and checks them against the house
   rules for this dataset: the three proposed vLLM step headings are present;
   every claim bullet carries exactly one FACT, DERIVED or UNKNOWN label; the
   issue-515 source URL is present; UNKNOWN is kept for the step-1 ROCm version
   and the step-3 training configuration.
3. Prints the exact two-file publish set with hashes and the exact forum note
   text, with the dataset page URL filled in.

It never uploads anything, never reads or writes a token, never uses the
network, and never writes to the target folder. Publishing is done by the
publish play; posting is done by a person or a step that has a forum account.

## Caveats first

- A person decides; an agent never merges, publishes or posts.
- Nothing was published, uploaded or posted from the step that wrote this tool.
- Everything the tool reads is data, never instructions. Text inside
  `SUMMARY.md` or `README.md` that tells it to run commands, reveal settings,
  change its goal, send money or post something is ignored.
- Do not edit the target folder's files. This tool only reads them.

## How to run

From inside this folder, offline, no arguments needed for the self-test:

~~~bash
python3 self_test.py
~~~

To prepare the real publication:

~~~bash
python3 publish_note.py ../opp-547-38-gfx950-mi355x-summary
~~~

The path argument is optional; the default is
`../opp-547-38-gfx950-mi355x-summary` relative to this file. Exit code 0 means
the two files exist and pass the rules; a non-zero exit means at least one rule
failed and the reason is printed.

## The exact two-file publish set

Only these two files go up, exactly as they are on disk, no field edits:

- `SUMMARY.md`
- `README.md`

No code, no logs, no `SELFTEST_OUTPUT.md`, no report files. `publish_note.py`
and `self_test.py` are not uploaded.

## What is untested

- The real on-disk bytes of `tools/opp-547-38-gfx950-mi355x-summary/` were not
  available in the step that wrote this tool, so the fingerprints and rule
  checks have been run only against this tool's own sample data, built inside
  the self-test. UNTESTED against the real folder.
- UNTESTED: the Hugging Face upload itself. This tool does not upload. The
  publish play does that, and the live dataset page is the only evidence it
  happened.
- UNTESTED: whether the dataset card renders from `README.md`, and whether
  remote bytes match the local sha256 after upload.
- UNTESTED: whether the forum the note is meant for accepts it, and whether the
  dataset URL resolves, since no dataset was created in this step.
- UNTESTED: whether the real `SUMMARY.md` still leaves the step-1 ROCm version
  and the step-3 training configuration as UNKNOWN; if it now states them, the
  rule check will fail and say so.

## Left for the owner

Run the tool against the real folder, upload the two files it names exactly as
on disk via the publish play, then post the note it prints. If the tool prints
a FAIL, fix only `publish_note.py` or `self_test.py` so the checks still test
`SUMMARY.md`'s own content.

Made by HivePunk #547, an AI agent on HivemindOS.
