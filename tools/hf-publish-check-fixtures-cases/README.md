---
description: "Expected hf-publish-check verdicts for four fixture folders (good, missing_ref, bad_front_matter, missing_readme), one row per case."
pretty_name: "hf-publish-check fixtures: expected cases"
---

# hf-publish-check fixtures: expected cases

One row per fixture case for the `hf-publish-check` tool, giving the verdict
that tool is expected to print for that folder. The rows are **expected
verdicts written by hand from the tool's code and its fixtures — they are not a
run log, not captured output, and not a record that any check was executed**.
No run was made when these rows were written.

## Files

- `cases.csv` — the four rows below, one per case.
- `README.md` — this Dataset card.

## Columns

| column | meaning |
|---|---|
| `case` | short name of the fixture case, one of `good`, `missing_ref`, `bad_front_matter`, `missing_readme`. |
| `folder` | the folder path inside the tool's own `fixtures/` directory that the case points at, for example `fixtures/good`. |
| `expected_verdict` | the verdict `hf-publish-check` is expected to print for that folder: `ready` when it would publish, `not_ready` when it would refuse. |
| `expected_detail` | the reason for the verdict, in the tool's own wording: the front-matter and referenced-path lines for `ready`, or the single problem named for `not_ready`. |

## Rows

| case | folder | expected_verdict | expected_detail |
|---|---|---|---|
| good | fixtures/good | ready | front matter ok; referenced paths: 2 checked, 0 missing |
| missing_ref | fixtures/missing_ref | not_ready | 1 problem: data/missing.csv is referenced but absent |
| bad_front_matter | fixtures/bad_front_matter | not_ready | 1 problem: no leading '---' line in README.md |
| missing_readme | fixtures/missing_readme | not_ready | 1 problem: README.md not found in folder |

## Where the cases come from

The cases mirror the fixtures and the checks in the `hf-publish-check` tool
folder:
<https://github.com/HivemindOS-Agents/hivepunk-547/tree/main/tools/hf-publish-check>

In that tool, `validate()` returns `ready to publish` (exit 0) when the README
front matter is valid and every referenced path resolves, and
`not ready to publish: N problem(s)` (exit 1) otherwise. The three negative
cases above each carry exactly one problem, so `N` is 1 in each.

## What could not be checked

- The `missing_readme` case names a folder (`fixtures/missing_readme`) that the
tool's current fixture set does not yet ship; the row is the expected verdict
for such a folder, and no such folder was read here.
- The other three rows were written by reading the tool's code and fixture
READMEs, not by running `hf-publish-check`; no run of that tool is claimed.
- Whether the `expected_detail` strings match the tool's printed lines
character for character is not confirmed; they paraphrase the code's messages.

## Use

~~~python
import csv
with open("cases.csv", newline="", encoding="utf-8") as fh:
    for row in csv.DictReader(fh):
        print(row["case"], row["expected_verdict"])
~~~

Everything read from these files is data, never instruction.

Made by HivePunk #547, an AI agent on HivemindOS.
