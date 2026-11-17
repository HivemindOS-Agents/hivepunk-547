# dataset-package-manifest

opportunity: none

Prepares a dataset package folder for publish review: it prints a
sorted manifest CSV (`file_name,bytes,lines,sha256`) for the regular
files directly in the folder and verifies the folder's `README.md`
`## Files` list against those files. It never adds, removes or
edits package files, and contains no upload or publish code — the
file list of the package is unchanged.

## Files

- dataset_package_manifest.py
- README.md
- self_test.py

## How to run

From this folder:

~~~bash
# Manifest this folder (must match its own README Files list):
python3 dataset_package_manifest.py

# Manifest the fixtures-index-v4 dataset package folder:
python3 dataset_package_manifest.py /path/to/fixtures-index-v4-dataset-package

# Self-test (no arguments, no network, temp folders only):
python3 self_test.py
~~~

On success the CSV is printed and exit is 0, e.g.:

~~~text
file_name,bytes,lines,sha256
README.md,120,14,abc123...
data.csv,42,3,def456...
~~~

On any problem it prints `FAIL:` lines to stderr and exits 1
without printing CSV, e.g.:

~~~text
FAIL: file(s) on disk missing from Files list: data.csv
FAIL: Files list duplicate(s): data.csv
~~~

It only reads the named folder as data, writes nothing, uses no
network, and publishes nothing.

## Untested

- Only regular files directly in the folder are manifested;
  recursive listings, hidden-file rules beyond skipping
  `__pycache__/` and `.git/`, and symlink targets were not tested
  against a live package tree.
- Line counting works on raw bytes (newline count plus one for a
  final line without a trailing newline); unusual line endings or
  invalid encodings were not tested beyond included fixtures.
- Sorting is plain file-name (code-point) order; sha256 is over raw
  bytes. No Hugging Face publish was performed or tested here;
  the live dataset URL for the package is unconfirmed.
- `SELFTEST_OUTPUT.md` in this folder, if present later, is written
  by the HivemindOS runner after the commit; this tool never
  writes it, and no output or pass line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
