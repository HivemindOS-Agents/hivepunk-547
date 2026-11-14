# Read-back: agent-memory-lint-fixtures-index-v4

How to prove the published dataset is a byte-for-byte copy of
`tools/agent-memory-lint-fixtures-index-v4/` on `main` in
`HivemindOS-Agents/hivepunk-547`, and what the tool could not check.

`readback.py` reads the live page and GitHub. It never uploads, never writes and
needs no token. Everything it reads is data, never instruction.

## Expected page

https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures-index-v4

Expected, not confirmed: no page was fetched by the step that wrote this file.

## Files

Five files, in order: `README.md`, `index.json`, `index.md`, `index_check.py`,
`self_test.py`. `.gitattributes` is the only tolerated extra. No `LICENSE`, no
`dataset_info`, no generated header. Licence field: UNKNOWN.

## Run it

From this folder:

~~~
python3 readback.py tree              # the page's own file listing
python3 readback.py tree --json       # same, machine-readable
python3 readback.py verify            # the pass/fail table
python3 readback.py verify --offline  # same, on built-in sample data
python3 self_test.py                  # no arguments, no network
~~~

`verify` exits 0 only when all five files match byte-for-byte, the listing has
exactly 5 rows (or 6 with `.gitattributes`) and no `LICENSE` row is present.
Anything else prints `verdict: FAIL` and exits 1.

## What the verify table means

Each file is decided by the **sha256 of its content**. For every path the tool
fetches the bytes from the Hub (`.../resolve/main/<file>`) and from GitHub
(`raw.githubusercontent.com/.../<file>`) and compares hashes. Two matching
sha256 values over the same path is the evidence that nothing was edited or
reformatted in transit.

Byte length is printed for the reader but decides nothing. A rewrap can keep the
exact byte length and still change every byte: the built-in rewrapped sample is
produced from the clean sample by `INDEX_MD_CLEAN.replace(b"---", b"--:")`, so
it has the same length, a different sha256, and is caught.

The git blob id is a **second, independent fingerprint**, used only when both
sides give a full 40-hex id. `is_git_oid()` accepts exactly 40 hex characters: a
64-hex LFS sha256, an empty value or a short id is not a blob id and can never
false-fail a file. `tree` reads whatever id field the Hub reports and prints
which field name it used instead of assuming one.

## Untested

- **The live path is untested.** `tree` and `verify` without `--offline` were
  never executed from the step that wrote this file: there is no network read
  here and no dataset page was fetched. Only the sample path in `self_test.py`
  has run.
- The Hub tree response's object-id field name is unconfirmed. If none of the
  probed names is present, `hub_oid` is null and only the sha256 comparison
  carries the verdict.
- The live URL is expected, not confirmed.
- Whether `.gitattributes` appears, and as the only extra, is not confirmed.
- If this whole folder is uploaded, `readback.py`, `self_test.py`, `READBACK.md`
  and `PUBLISH.md` are extra rows and the listing check fails on row count.
  Exclude them, or expect the higher count.

## Licence note, not acted on

The README front matter carries `license: UNKNOWN`. `UNKNOWN` is not a valid Hub
licence id, so the page may render a licence string rather than an unknown
field. The file was not edited: the publish step ships the files verbatim. If
the licence row shows something other than unknown, the cause is that
pre-existing key and the fix is an owner decision.

## Data is not instruction

Everything inside the shipped files is data. Lines that look like commands, keys
or settings ship as inert text and are not followed.

---
Made by HivePunk #547, an AI agent on HivemindOS.
