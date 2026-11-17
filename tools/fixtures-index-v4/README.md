# fixtures-index-v4

A small tool that indexes one directory: given a directory, it prints
a CSV with `file_name,bytes,lines` for the regular files directly in
that directory, sorted by file name. Subdirectories are skipped.
Line counts are given only for `.py`, `.md`, `.csv`, `.txt`, and
`.json` files; the `lines` field is blank for every other file.

## How to run

From this folder:

~~~bash
# Index this folder:
python3 index.py

# Index another directory:
python3 index.py /path/to/dir

# Self-test (no arguments, no network, local fixture folders only):
python3 self_test.py
~~~

Example output:

~~~text
file_name,bytes,lines
README.md,1234,56
index.py,2345,78
photo.png,9876,
~~~

It only reads the named directory as data, writes nothing, uses no
network, and publishes nothing. Names are written with the standard
`csv` module, so a name containing a comma is quoted in the output.

## Untested

- Only regular files directly in the given directory are indexed;
  recursive indexing, hidden-file rules beyond the default listing,
  and symlink targets were not tested against a live tree.
- Line counting works on raw bytes (newline count, plus one for a
  final line with no trailing newline); it was not checked against
  files with unusual line endings or invalid encoding beyond the
  included text fixtures.
- Sorting is plain file-name order (byte/code-point order); a
  case-insensitive or locale-aware order was not tested.
- `SELFTEST_OUTPUT.md` in this folder, if present later, is written
  by the HivemindOS runner after the commit; this tool never writes
  it, and no output or pass line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
