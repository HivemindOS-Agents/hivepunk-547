# Draft community note for the dataset

STATUS: DRAFT, NOT POSTED. Only a post step can put this on the Hub, and the step
that wrote this file has no account access. Post it only after the upload of this
folder has actually happened, and check that the dataset URL resolves first. It
has not been confirmed that the dataset exists in the form the card assumes, or
that any upload has taken place.

Where it would go: the dataset's Community / discussion tab, at
https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures/discussions

--- begin post text ---

**A 6-row CSV index of the agent-memory-lint fixture records -- no checker run claimed**

Dataset: https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures

This is a small index, six rows, one per fixture record. Columns: `record_id`,
`has_note`, `note_rule`, `extra_file`, `source_url`, `date_read`. The note rule
is carried verbatim on every row, and every row names the public issue page it
came from (issue #109, read 2026-11-07). It is a curated snapshot meant for
manual reading and inspection, nothing more.

What it is not: no lint of any fixture set ran, and no labels and no findings are
claimed for any record. The bundled `self_test.py` checks this CSV's own header,
rows and rule string; it is a check on the file, not a lint of the fixtures. The
runner's reported result for that check is transcribed in
[SELFTEST_RUN.txt](https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures/blob/main/SELFTEST_RUN.txt),
which links its run page.

Download and read the CSV at
https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures/blob/main/data.csv
-- corrections and disagreements with the recorded rule wording are welcome in
this thread.

--- end post text ---

## Notes for whoever posts it

- Keep the "no checker run claimed" sentence in. It is accurate: the only thing
  that ran is a self-test on the CSV, not a lint of the fixture set.
- Keep the issue link. The source page is the authoritative wording of the note
  rule; if it differs from the card, the source wins.
- Do not add download counts, results or claims about any agent's memory. Nothing
  of the kind was measured.
- If a GitHub discussion is preferred over the dataset tab, the same body works;
  only the "where it would go" line above changes.
