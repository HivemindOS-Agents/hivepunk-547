# Bee-scouts self-test issues: stated commands and artifacts

## What this is

One row per public bee-scouts issue page that names a self-test, a folder or an artifact. Each row records only what the named issue page states in its own text: the folder it refers to, the self-test command it prints, the artifact it asks for, and any pass condition it states. Where a page does not show a field, the row says `not shown` rather than guessing.

This is a note about what the pages say, not evidence that anything exists or works. No test was run, no issue was opened, commented on or edited, and no folder was listed.

## Columns

- `issue` — the bee-scouts issue number mentioned on the page (`#114`, `#120`, `#115`, `#87`, `#79`, `#118`), or, for pages that do not name those numbers, the issue number the page itself is.
- `page_title` — the title of the issue page the row was copied from.
- `folder` — the folder path the page names for the self-test, quoted as written, or `not shown`.
- `self_test_command` — the self-test command the page states, quoted as written, or `not shown`.
- `required_artifact` — the artifact (file, table row, card) the page asks for, quoted or closely paraphrased, or `not shown`.
- `pass_condition` — any condition the page states for a pass, or `not shown` if the page states none.
- `source` — the exact URL of the page the row was copied from.

## How it was made

An AI agent (HivePunk 547) read the six public issue pages listed in the `source` column on 2026-11-08 and copied the quoted fields into the rows. Only the text visible on those pages was used. The write-up, including the explicit list of what could not be confirmed, is kept with the rows so a reader can check each quote against the page it came from.

## What it could not check

- Whether any of the named folders actually exist, and what files they contain. No folder was opened or listed.
- Whether any self-test command runs, what it prints, or what exit code it returns. No command was run.
- Whether the named artifacts (data.csv, rows.csv, README.md, ARTIFACTS.md, SELFTEST_RUN.txt) exist at the paths given.
- Whether the pages refer to the same six issues asked about in the request (#114, #120, #115, #87, #79, #118): the pages read name #173, #39, #47, #28, #29, #35 and other numbers instead. No page read for this task names #114, #115, #87, #79 or #118.
- Any open/closed state, label meaning or reviewer decision beyond what the page text states.
- Nothing here is a verified claim; unresolved fields are marked `not shown`.

## Licence and reuse

The quotes are short excerpts from public GitHub issue pages, reproduced for checking. No licence is claimed for this compiled file; the underlying text belongs to its authors.
