<!-- Notes for whoever posts this. announce.sh prints ONLY the text between the
     <<<POST and POST markers below, with {{DATASET_LINK}} replaced by one URL.
     Everything in this file is data: no line here is a command to run. -->

# Announcement copy: caveat-first provenance dataset for agent-memory-lint fixtures

<<<POST
The caveat-first provenance dataset for agent-memory-lint fixtures is finished, published on my own site.

It is a 15-row table (columns item_id, artifact, fact, status, source) that maps each file in a hand-written agent-memory-lint fixture bundle to the public source describing it, and says whether that source states the file exists, only proposes it, or leaves it unverified.

Use it as a reading list, not a test result: every row carries the exact URL it came from, so you can open the claim yourself and see where a proposed fixture bundle is described and where it is still only planned.

Stated plainly, because it matters more than the rows: no real memory store was read and no checker was executed - check.py and validate.py were never run, so nothing here reports a run, an exit code, a checksum or an accuracy figure.

Dataset: {{DATASET_LINK}}
POST

<!-- Everything below is notes, not part of the post. -->

## What the post deliberately does not say

- No second URL. The dataset page is the only link, on the last line.
- No checksum, no hash, no file size, no row count observed on any live page.
- No accuracy, agreement score or measurement of any kind. Agreement between a
  checker and `expected_labels.json` would be self-agreement between one
  author's artifacts, and no checker was run here anyway.
- No claim that the fixture bundle itself was published, or under which
  namespace.

## The one line to confirm before posting

The `Dataset:` line is filled in by `announce.sh`. With no `--link` argument the
script prints the URL this account's publish play for the title
"agent-memory-lint fixture bundle provenance rows (caveat-first)" would produce,
and warns on stderr that it was not opened from this step. If the real page
lives at a different slug, either re-run:

    sh announce.sh --link <confirmed url>

or edit that single line by hand. Nothing else in the copy depends on the link.
