# dataset-manifest-check

opportunity: none

A small read-only Python checker comparing a dataset manifest
JSON file list against a supplied public file-listing text
file. It compares the exact normalised sets and reports
d daplicates on either side, PASS/FAIL counts, and the sorted
differences (`only_in_manifest`, `only_in_listing`). It writes
nothing and uses no network.

Live datasets were not checked by this tool: it does not fetch
Hugging Face, GitHub, or any other page, does not verify that
a supplied listing is complete or current, and does not check
file contents, sizes, or hashes. It only compares the two
lists you give it. If the supplied listing is stale or
incomplete, the result reflects that listing, not the live
dataset.

## Files

- dataset_manifest_check.py
- README.md
- self_test.py

## How to run

From this folder:

~~~bash
# Compare a manifest against a supplied listing:
python3 dataset_manifest_check.py /path/to/manifest.json /path/to/listing.txt

# Strip a common prefix (e.g. a dataset folder prefix) first:
python3 dataset_manifest_check.py /path/to/manifest.json /path/to/listing.txt --strip-prefix dataset/

# Self-test (no arguments, no network, temp files only):
python3 self_test.py
~~~

On success it prints e.g. `PASS: manifest.json vs listing.txt
(manifest: 3, listing: 3, common: 3, only_in_manifest: 0,
only_in_listing: 0, duplicates_manifest: 0,
duplicates_listing: 0)` and exits 0. Otherwise it prints one
`FAIL:` line per difference or duplicate plus a summary line
with the same counts and exits 1, e.g.:

~~~text
FAIL: only in manifest: data/missing.csv
FAIL: only in listing: data/extra.txt
FAIL: manifest.json vs listing.txt (manifest: 3, listing: 3, common: 2, only_in_manifest: 1, only_in_listing: 1, duplicates_manifest: 0, duplicates_listing: 0)
~~~

Manifest formats: JSON as a list of path strings, or an object
with a `files` list whose entries are strings or objects with a
`path`/`file`/`filename`/`name` field.

Listing format: one path per line; blank lines and `#` comment
lines are ignored and a leading `- `, `* ` or `+ ` bullet
marker is stripped.

Normalisation on both sides: strip whitespace, convert
backslashes to slashes, remove leading `./` and `/`, and remove
`--strip-prefix` when given. PASS requires equal unique sets
and no duplicates on either side.

It only reads the two named files, writes nothing, uses no
network, and publishes nothing.

## Untested

- Untested against live Hugging Face datasets or pages: no live
  manifest or file listing was fetched or compared, and remote
  listings in other formats (HTML pages, API JSON, tree views
  with sizes/dates on the same line) are not parsed; supply a
  plain one-path-per-line text file instead.
- File contents, byte sizes, checksums, and whether listed
  files actually exist on disk or remotely were not tested.
- Manifest shapes other than a list or a `files` list (nested
  objects, YAML, archives) report an invalid-manifest failure.
- `SELFTEST_OUTPUT.md` in this folder, if present later, is
  written by the HivemindOS runner after the commit; this tool
  never writes it, and no output or pass line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
