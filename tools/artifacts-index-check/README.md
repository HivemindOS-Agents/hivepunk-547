# artifacts-index-check

opportunity: none

Checks an `ARTIFACTS.md` artifact index: parses artifact entries
(bullet lines `- ...` / `* ...` and table rows `| ... |`), then
verifies that every listed local file exists (relative to the
directory containing `ARTIFACTS.md`) and that every listed URL
is well-formed. Reachability is not checked; there is no network
use. It prints specific problems or `ok`.

## Files

- artifacts_index_check.py
- README.md
- self_test.py

## How to run

From this folder:

~~~bash
# Check ./ARTIFACTS.md in the current directory:
python3 artifacts_index_check.py

# Check a named index file or its folder:
python3 artifacts_index_check.py /path/to/ARTIFACTS.md
python3 artifacts_index_check.py /path/to/folder

# Self-test (no arguments, no network, temp files only):
python3 self_test.py
~~~

On success it prints e.g. `ok: ARTIFACTS.md (2 entries, 2 local
file(s), 2 URL(s))` and exits 0. Otherwise it prints one `FAIL:`
line per specific problem and exits 1, e.g.:

~~~text
FAIL: ARTIFACTS.md: line 3: listed local file not found: notes/missing.md
FAIL: ARTIFACTS.md: line 4: malformed URL 'https://': missing host
FAIL: ARTIFACTS.md: no artifact entries found (expected bullet or table entries)
~~~

A valid index looks like:

~~~markdown
# Artifacts

- Report | `notes/report.md` | https://example.org/report
- Data | [data](data/items.csv) | https://example.org/data

| Tool | `tools/check.py` | https://example.org/tool |
~~~

Local paths are taken from backticked path-like strings,
markdown link targets that are not URLs, and table cells that
look like paths. URLs come from `http://`/`https://` tokens and
markdown link targets. A well-formed URL needs an http/https
scheme, a non-empty host (dotted or `localhost`), no spaces or
invalid characters, and a valid port if given.

It only reads the named index (and stats the listed files),
writes nothing, uses no network, and publishes nothing.

## Untested

- Untested against the live `ARTIFACTS.md` in this repository:
  the entry format above is the documented contract, and an
  index using a different format (headings-only entries, multi-
  line entries, bare titles with no path/URL) will report no
  entries or miss items. That mismatch is unconfirmed.
- Only well-formedness is checked; a well-formed URL that is
  dead, redirected, or wrong in content will still pass.
- Symlinks, case-insensitive filesystems, and Windows paths
  were not tested; on such systems existence results may differ.
- `SELFTEST_OUTPUT.md` in this folder, if present later, is
  written by the HivemindOS runner after the commit; this tool
  never writes it, and no output or pass line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
