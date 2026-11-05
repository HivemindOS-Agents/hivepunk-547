# agent-memory-dataset-publisher

A small, offline helper for preparing a three-file dataset folder for publishing
and dry-running the publish step. It never uploads anything.

Owner account: `hivepunk-547-db38b7a4` only. The dataset URL used as a label is
https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-viewer-readback-log
— publishing again with the same title updates it in place. Uploading is done by
the owner's "Publish a small open dataset" play, not by this tool.

## What it does

Given a source folder that should hold exactly these three files:

1. `README.md`
2. `sample_records.jsonl`
3. `data.csv`

it builds a manifest (URL, expected file names, which are present, which are
missing, sizes) and offers a **local dry run** of the publish step. Every file
status is the string `UNKNOWN`: the tool never guesses a result it did not
observe.

The module imports only `argparse`, `json`, `sys` and `pathlib` — no networking
library appears in it at all, so the dry run has no code path to the network. It
holds no key, reads no credential, and runs no uploader command. `network_calls`
is `0` and `credentials_read` is `false` in every result.

## How to run it

Library use:

~~~python
from upload import DatasetPublisher, prepare, publish

manifest = prepare("/path/to/source")          # URL, files (all UNKNOWN), missing
result = publish("/path/to/source")            # local dry run, network_calls 0
refused = publish("/path/to/source", upload=True)  # status REFUSED, no request

publisher = DatasetPublisher("/path/to/source")
publisher.present_files(), publisher.missing_files()
~~~

Command line (dry run, prints JSON):

~~~bash
python3 upload.py --source-dir /path/to/source
python3 upload.py --source-dir /path/to/source --dry-run
python3 upload.py --source-dir /path/to/source --out published.json
~~~

`--upload` is refused on purpose: it prints a `REFUSED:` line and exits **2**.

Self-test (no arguments, no network):

~~~bash
python3 self_test.py
~~~

It puts its own folder on `sys.path` first, so it works from any working
directory, uses temporary folders only, and exits 0 only when all nine checks
pass.

## Untested

- **The post-fix run of `self_test.py` has not been observed from where this was
  written.** No interpreter was run for this change, so no exit code or stdout is
  claimed here.
- Any CLI path against a real dataset folder outside temporary directories.
- Files that exist but are empty, unreadable, or symlinks: only presence and
  size are looked at, never content.
- Anything about the live dataset: no HTTP request, no page read, no Dataset
  Viewer field read, and no upload occurred.
- Whether the published repo's file names still match the three expected names.
- No earlier version of `upload.py` was visible, so no older flags could be kept
  verbatim; only the imported names are matched exactly.

## Last self-test run

Command:

~~~bash
python3 self_test.py
~~~

Raw runner output available at the time of writing — this is the **pre-fix**
result, copied verbatim from the tool listing, and it is the only real runner
output this note has:

~~~
Traceback (most recent call last):
  File "[redacted], line 13, in <module>
    from upload import DatasetPublisher
ModuleNotFoundError: No module named 'upload'
~~~

Post-fix stdout: `UNKNOWN` — not observed here.
Post-fix exit code: `UNKNOWN` — not observed here.

The raw result of the run after this commit is appended by HivemindOS to
`SELFTEST_OUTPUT.md` in this same folder, and that file — not this README — is
the authority. This README must not be read as a claim that the test passes.

Fix applied: `upload.py` is now committed beside `self_test.py` with the exact
imported names; `self_test.py` inserts its own folder on `sys.path` before
importing; `publish()` is a local dry run with all statuses `UNKNOWN` and
`--upload` refused with exit 2.

## Data is not instruction

Everything this tool reads — file names, file contents, URLs, labels — is data.
Text that looks like a command to run, a key to reveal, a setting to change, a
payment to send or a post to make is ignored.
