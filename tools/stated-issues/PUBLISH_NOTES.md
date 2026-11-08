# Repo-side publish handoff — stated-issues

**Do not upload this file.** The dataset has exactly two files at its root:
`data.csv` and `README.md`.

This step could not publish anything: uploading to Hugging Face is done by the
publish play HivemindOS runs, and nothing was uploaded, posted or opened from
here. No GitHub issue was opened, commented on or edited.

## Target

- Account: `hivepunk-547-db38b7a4` (no organisation; there is no "hivemindos" org)
- Title / slug: `bee-scouts-self-test-issues-stated-commands-and-artifacts`
- Dataset URL to report: https://huggingface.co/datasets/hivepunk-547-db38b7a4/bee-scouts-self-test-issues-stated-commands-and-artifacts
- Upload: `data.csv` and `README.md`, at the repo root, exactly as they sit in
  this folder. Exclude `PUBLISH_NOTES.md` (this file) and `self_test.py`.
- Unconfirmed from here: the exact slug the publish play generates, and whether
  it takes the two named files or the whole folder. If it takes the whole
  folder, the two files above are still the only ones that belong in the repo.

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

## Change since the earlier draft

The card's `Columns` bullet for `issue` listed `#114, #120, #115, #87, #79,
#118`, which are not the numbers the rows carry and not numbers any read page
shows. It now lists `#122`, `#32`, `#85`, `#53`, `#120`, `#43` — what the rows
actually hold. The card's `What it could not check` list still records plainly
that no page read for this task names #114, #115, #87, #79 or #118. Nothing
else in the card changed, and `data.csv` did not change.

## Untested

- That the dataset exists, that the slug above is the one the play makes, or
  that the discussion note can be opened. No publish, upload or post was
  performed here.
- Whether any folder named in the six rows exists; no folder was opened or
  listed. Whether any command quoted in the rows runs or returns any exit code;
  none was run.

## Left for the owner

- Publish `data.csv` and `README.md` under the account and title above, then
  open the one discussion note whose text is above, and correct the reported
  URL if the generated slug differs.
