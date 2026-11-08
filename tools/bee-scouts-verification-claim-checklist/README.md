# bee-scouts verification-claim checklist

A checklist of what the finished stated-issues package claims and what would
actually prove each claim. Every claim is one the six sourced issue pages state;
every verdict says how far the package can support it, and never further.

Intended Hugging Face dataset URL (slug **unconfirmed**):
https://huggingface.co/datasets/hivepunk-547-db38b7a4/bee-scouts-verification-claim-checklist
Account: `hivepunk-547-db38b7a4`.

## Files

The dataset holds exactly two files at its root: `data.csv` and this
`README.md`. No script, notes or run log ships with it.

## Columns

- `claim` — the claim the stated-issues package makes, quoted from the issue/lines it draws on.
- `where_it_appears` — where in the package the claim sits.
- `what_would_prove_it` — the smallest thing that would turn the claim into a checked one.
- `what_is_missing` — what is missing today.
- `verdict` — one of `shown`, `unshown`, `none-observed`.
- `source` — the public issue page the row was drawn from.

## How the verdicts are worded

- `shown` — the package text supports the claim as words on the page; nothing beyond the wording is asserted.
- `unshown` — the claim says something that needs a run, a date or a file we do not have.
- `none-observed` — no observation of any kind backs the claim; none was made.

## What could not be checked

- Whether any folder named in this checklist exists, or what files it contains. No folder was opened or listed.
- Whether any command quoted on the source pages runs, what it prints, or what exit code it returns. No command was run.
- Whether the six named source pages still show the text this checklist quotes; no page was fetched for this file.
- Whether the dataset exists at the URL above, or that a publish run generates this slug.
- Whether the self-test has been run and passed; its first real output belongs in a run log, pasted from the run, not retyped from expectation.

## Not said here

No test was run, no folder was opened or listed, and no GitHub issue was opened,
commented on or edited while making this checklist. It is a note about what the
pages say, not evidence that anything works.
