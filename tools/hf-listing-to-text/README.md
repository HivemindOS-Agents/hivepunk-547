# hf-listing-to-text

opportunity: none

A small read-only Python converter that turns a supplied
Hugging Face dataset file-listing JSON into sorted
one-path-per-line text, suitable as input to
`dataset-manifest-check`.

## How to run

From this folder:

~~~bash
# To stdout:
python3 hf_listing_to_text.py /path/to/listing.json

# To a file (input for dataset-manifest-check):
python3 hf_listing_to_text.py /path/to/listing.json -o listing.txt
python3 ../dataset-manifest-check/dataset_manifest_check.py manifest.json listing.txt

# Strip a common prefix, or keep duplicates:
python3 hf_listing_to_text.py listing.json --strip-prefix dataset/
python3 hf_listing_to_text.py listing.json --keep-duplicates

# Self-test (no arguments, no network, temp files only):
python3 self_test.py
~~~

Accepted JSON shapes: an HF API list of objects with
`rfilename`, `{siblings: [{rfilename: ...}]}`,
`{files: [...]}` (strings or objects with
`rfilename`/`path`/`file`/`filename`/`filepath`/`name`),
or a plain list of path strings.

Behaviour: blank lines and `#` comment lines are skipped,
a leading `- `, `* ` or `+ ` bullet is stripped,
backslashes become slashes, leading `./` and `/` are
removed, `--strip-prefix` is removed when given, and the
output is sorted lexicographically, one path per line.
Duplicates are removed by default with a note on stderr;
`--keep-duplicates` keeps them. Invalid, empty, missing or
wrong-shape input exits 1 with a clear `FAIL:` line;
usage errors exit 2. Success exits 0. An object entry with
none of the accepted path fields (for example `{size: 3}`)
is invalid input and exits 1 the same way.

## Untested

- Supplied JSON only: no network, no Hugging Face fetch,
  and no verification that the supplied listing is complete,
  current, or matches any live dataset. File contents,
  sizes and hashes are never checked.
- Untested against a real Hugging Face API response: the
  HF API shape is handled from its documented `rfilename`
  field on synthetic fixtures, not from a fetched response;
  any other API fields or pagination are ignored.
- Listings in other formats (HTML pages, tree views with
  sizes/dates, YAML) are not parsed; supply JSON as above.
- `SELFTEST_OUTPUT.md`, if present later, is written by the
  HivemindOS runner; this tool never writes it, and no
  pass line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
