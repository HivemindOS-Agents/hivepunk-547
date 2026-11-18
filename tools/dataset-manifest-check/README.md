# dataset-manifest-check

opportunity: none

A small read-only Python checker for a dataset manifest. It
verifies that every file listed in the manifest exists locally
under a root directory, and flags files under that root that are
not listed in the manifest. It prints counts and a PASS/FAIL
summary, and writes nothing.

Live Hugging Face pages were not checked by this tool: it does
not use the network, does not fetch any dataset page or file,
and does not verify that local files match a remote dataset.
It only checks local existence against the manifest.

## Files

- dataset_manifest_check.py
- README.md
- self_test.py

## How to run

From this folder:

~~~bash
# Check a manifest; root defaults to the manifest's folder:
python3 dataset_manifest_check.py /path/to/manifest.txt

# Check a manifest against a different root folder:
python3 dataset_manifest_check.py /path/to/manifest.json --root /path/to/data

# Report unlisted files as NOTE instead of failing:
python3 dataset_manifest_check.py /path/to/manifest.csv --allow-unlisted

# Self-test (no arguments, no network, temp files only):
python3 self_test.py
~~~

On success it prints e.g. `PASS: manifest.txt (listed: 3,
present: 3, missing: 0, unlisted: 0)` and exits 0. Otherwise it
prints one `FAIL:` line per specific problem plus a summary line
with the same counts and exits 1, e.g.:

~~~text
FAIL: manifest.txt: listed file not found: data/missing.csv
FAIL: manifest.txt: unlisted file: data/extra.txt
FAIL: manifest.txt (listed: 3, present: 2, missing: 1, unlisted: 1)
~~~

Manifest formats (auto-detected):

- JSON (`.json`): a list of path strings, or an object with a
  `files` list whose entries are strings or objects with a
  `path`/`file`/`filename`/`name` field.
- CSV (`.csv`): a header row containing a `path`, `file`,
  `filename` or `name` column; each following row lists one path.
- Text (`.txt`, `.tsv`, `.md`, extensionless): one path per line;
  blank lines and `#` comment lines are ignored and a leading
  `- `, `* ` or `+ ` bullet marker is stripped.

Listed paths must be relative and stay under the root (`..` and
absolute paths are rejected). Unlisted files are found by walking
the root recursively (directory symlinks are not followed); the
manifest file itself and any other `manifest.*` file are excluded.
Duplicate listed entries are checked once and reported as a NOTE.

It only reads the manifest and stats the files under the root,
writes nothing, uses no network, and publishes nothing.

## Untested

- Untested against live Hugging Face datasets or pages: no live
  dataset manifest or folder was read by this tool, and remote
  file lists were not compared with local files (see above).
- Manifests using other shapes (nested objects, YAML, archives)
  are not supported and will report an invalid-manifest failure
  rather than a partial check.
- Hidden files, permissions-denied folders, and broken symlinks
  under the root were not tested; unreadable folders are
  skipped by the walk and broken symlinks are not counted as
  files.
- `SELFTEST_OUTPUT.md` in this folder, if present later, is
  written by the HivemindOS runner after the commit; this tool
  never writes it, and no output or pass line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
