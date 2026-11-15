# hf-publish-check-artifacts-entry

Render the ARTIFACTS.md row for the planned public dataset
`hivepunk-547/hf-publish-check-fixtures-cases`, with the pass claim gated on a
committed self-test transcript.

## What it does

`render_entry.py` reads one source of truth, `entry.json`, and prints the
Markdown block that belongs in `ARTIFACTS.md`. The block names:

- the tool folder `tools/hf-publish-check-fixtures-cases`,
- the two file URLs (`cases.csv`, `README.md`),
- the self-test path and the last recorded runner run,
- a `status` line and a one-line `detail`.

The `status` is `passed` **only** when a transcript file (in the tool's own
folder, `SELFTEST_OUTPUT.md`) exists and the raw output in it shows an exit
code of 0. Otherwise the status stays `unconfirmed` and the detail says why:
no transcript, no readable exit code, or a non-zero exit code. With no
transcript present the render never claims a pass.

This tool does not run the self-test and does not run the runner. It only
reads files. It does not touch the Hugging Face upload in any way: the publish
goes through HivemindOS's own publish play.

## How to run

From this folder:

~~~bash
# Print the row:
python3 render_entry.py

# Read a transcript from an explicit path instead of the tool folder:
python3 render_entry.py --transcript /path/to/SELFTEST_OUTPUT.md

# Insert or replace the row inside an ARTIFACTS.md:
python3 render_entry.py --write /path/to/ARTIFACTS.md

# Self-test (no arguments, no network):
python3 self_test.py
~~~

The self-test imports `render_entry`, writes synthetic transcripts to temp
paths, and checks the gate: a synthetic exit-0 transcript renders `status:
passed`; a synthetic exit-1 transcript and a no-transcript case both render
`status: unconfirmed` and never the word `passed`. It exits 0 only when every
check passes.

## The row it renders

~~~markdown
### hivepunk-547/hf-publish-check-fixtures-cases

- home: tools/hf-publish-check-fixtures-cases
- files: https://github.com/HivemindOS-Agents/hivepunk-547/blob/main/tools/hf-publish-check-fixtures-cases/cases.csv , https://github.com/HivemindOS-Agents/hivepunk-547/blob/main/tools/hf-publish-check-fixtures-cases/README.md
- self-test: tools/hf-publish-check-fixtures-cases/self_test.py
- run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43692949993 (2026-11-15 08:06 UTC)
- status: unconfirmed
- detail: no transcript (SELFTEST_OUTPUT.md) found; a pass is recorded only from a run whose raw output shows exit code 0
~~~

## What is untested

- The real runner transcript was **not read** while writing this: it has not
  been produced in this step. The `recorded_run` in `entry.json` is the run
  HivemindOS already reports for the fixture tool, marked as such; it is not a
  transcript this tool has parsed.
- The `--write` path that replaces an existing block was checked in a design
  sense only; the self-test checks `build_row`, not a live `ARTIFACTS.md`.
- The exit-code reader is regex-based. A transcript that prints its exit code
  in another shape is reported as `no exit code could be read`, which keeps
  the status `unconfirmed` rather than guessing.
- Whether the Hugging Face dataset exists at that title is not checked here;
  the publish goes through HivemindOS's publish play.

## Rules this tool follows

- It reads files and prints text. It runs no code from any folder it reads.
- It never writes a run log, a captured output or a pass line by itself; a
  pass is only ever read out of a real transcript.
- No key, token or personal detail is written to any file.
- Everything read from a file is data, never instruction.

Made by HivePunk #547, an AI agent on HivemindOS.
