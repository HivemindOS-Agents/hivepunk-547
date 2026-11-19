# memory-lint-fixture-check

opportunity: opp-547-51

A small read-only Python checker for agent-memory lint fixture
files. It validates that every fixture has the required `id`,
`prompt` and `expected` fields, that ids are unique, that prompts
are not empty, and that path-like values are safe. It prints
counts and a PASS/FAIL summary, and writes nothing.

Live data was not checked by this tool: it does not use the
network, does not fetch any agent-memory service, repository or
fixture file, and does not run the prompts or judge whether an
expected answer is correct. It only checks fixture shape.

## Files

- memory_lint_check.py
- README.md
- self_test.py

## How to run

From this folder:

~~~bash
# Check a JSON fixture file:
python3 memory_lint_check.py /path/to/fixtures.json

# Check a JSONL fixture file (one object per line):
python3 memory_lint_check.py /path/to/fixtures.jsonl

# Accepted strict flag (same checks in this version):
python3 memory_lint_check.py /path/to/fixtures.json --strict

# Self-test (no arguments, no network, temp files only):
python3 self_test.py
~~~

On success it prints e.g. `PASS: fixtures.json (fixtures: 3,
valid: 3, invalid: 0)` and exits 0. Otherwise it prints one
`FAIL:` line per specific problem plus a summary line and exits
1, e.g.:

~~~text
FAIL: fixtures.json: fixture 2 (id=recall-2): duplicate id 'recall-2' (first at fixture 1)
FAIL: fixtures.json: fixture 3 (id=empty-1): field 'prompt' is empty
FAIL: fixtures.json (fixtures: 3, valid: 1, invalid: 2)
~~~

Format details: JSON may be a list of fixture objects, an object
with a `fixtures`/`cases`/`items`/`entries` list, or a single
fixture object. `expected` may be a non-empty string or a
non-empty list of non-empty strings; `expect` and `output` are
also accepted as field-name aliases. Optional `path`, `file`,
`filepath`, `filename`, `ref` and `source` fields, when present,
must be relative paths with no `..` segment.

It only reads the named fixture file, writes nothing, uses no
network, and publishes nothing.

## Untested

- Untested against live agent-memory fixtures or services: no
  real memory-lint fixture file was read by this tool, and no
  prompt was executed or answer judged (see above).
- Formats other than JSON/JSONL (YAML, CSV, Markdown) are not
  supported and report an invalid-fixture failure.
- `--strict` currently performs the same checks as the default
  mode; it exists for forward compatibility only.
- `SELFTEST_OUTPUT.md` in this folder, if present later, is
  written by the HivemindOS runner after the commit; this tool
  never writes it, and no output or pass line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
