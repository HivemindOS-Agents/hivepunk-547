# Repo-side publish notes — stated-issues

This file sits beside the dataset files in the tool folder. It is repo-side only:
**do not upload this file**. The dataset has exactly two files at its root,
`data.csv` and `README.md`.

## Target

- Account: `hivepunk-547-db38b7a4` (no organisation; there is no "hivemindos" org)
- Title / slug: `bee-scouts-self-test-issues-stated-commands-and-artifacts`
- Dataset URL to report: https://huggingface.co/datasets/hivepunk-547-db38b7a4/bee-scouts-self-test-issues-stated-commands-and-artifacts
- Files: `data.csv` (header plus the 6 copied rows) and `README.md` (the card),
  both at the repo root
- Unconfirmed from here: the exact slug the publish play generates, and whether
  the uploader takes this whole folder or the two named files. If it takes the
  whole folder, this file must be excluded.

## Discussion note to open on the dataset

Title: Compiled from six bee-scouts issue pages — nothing was run

Body:

Six public bee-scouts issue pages were read on 2026-11-08 and only what they
state was copied: the folder each one names, the self-test command it prints,
the artifact it asks for and any pass condition; a field a page does not show is
marked `not shown`. No test was run and no folder was opened: none of the
folders named on those pages was listed, and no self-test command printed here
was executed. This is a note about what the pages say, not evidence that
anything exists or works. Dataset:
https://huggingface.co/datasets/hivepunk-547-db38b7a4/bee-scouts-self-test-issues-stated-commands-and-artifacts

## Known deviation, left in place

The card's `Columns` bullet for `issue` lists the numbers `#114, #120, #115,
#87, #79, #118` while the rows carry the numbers the read pages actually show
(`#122, #32, #85, #53, #120, #43`). The card's `What it could not check`
section already states that no page read for this task names #114, #115, #87,
#79 or #118. The card goes up as drafted; this note is the flag.

## Untested

- That the dataset exists, that the slug above is the one the uploader makes,
  or that the discussion note can be opened: none of that happens from this
  repo step, and no publish, upload or post was performed here.
- Whether any folder named in the rows exists, and whether any command in the
  rows runs or returns any exit code. None was run.

## Left for the owner

- Publish `data.csv` and `README.md` under the account and title above, then
  open the one discussion note whose text is above; confirm the resulting slug.
- No GitHub issue was opened, commented on or edited, and no bee-scouts folder
  was opened or listed.
