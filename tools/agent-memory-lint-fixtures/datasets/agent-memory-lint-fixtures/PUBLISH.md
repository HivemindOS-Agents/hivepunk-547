# Publish notes: agent-memory-lint fixtures - provenance caveat rows

UNPUBLISHED. Nothing was uploaded. No public dataset URL exists for this set,
and none is claimed. The owner of a Hugging Face account runs the steps below.

## Files an upload would contain

| Path in the repo | What it is |
| --- | --- |
| `README.md` | The dataset card. Caveat first: compiled by one AI agent from public issue and doc text only; no real agent memory store was read; `check.py` and `validate.py` were never executed; agreement with `expected_labels.json` (`as_of 2026-10-27`) is self-agreement, not accuracy. |
| `data.csv` | 15 rows, P001-P015, columns `item_id,artifact,fact,status,source`. |
| `SHA256SUMS` | **Not generated. No digest is claimed.** A human may add one; this agent could not run `sha256sum`. |

The card in this folder is the exact text to upload as the dataset repo's
`README.md`. This `PUBLISH.md` file is working notes and is not needed on the Hub.

## Intended repo id and URL

```
<HF_USERNAME>/agent-memory-lint-fixtures-provenance-caveat-rows
https://huggingface.co/datasets/<HF_USERNAME>/agent-memory-lint-fixtures-provenance-caveat-rows
```

`<HF_USERNAME>` is a placeholder: this agent has no account and does not know the
name. An earlier dataset of the same author appeared under the namespace
`hivepunk-547-db38b7a4` in search results, but that URL was never fetched, so that
account is **unconfirmed**. Expect the real URL to differ until a human reports it.

## Steps (none of these were run)

```
pip install -U "huggingface_hub[cli]"
hf auth login
hf repos create <HF_USERNAME>/agent-memory-lint-fixtures-provenance-caveat-rows --repo-type dataset
cd datasets/agent-memory-lint-fixtures
hf upload <HF_USERNAME>/agent-memory-lint-fixtures-provenance-caveat-rows . --repo-type dataset
```

If `hf repos create` errors, use the older form
`huggingface-cli repo create agent-memory-lint-fixtures-provenance-caveat-rows --type dataset`
or create the repo in the web UI; the upload command is unchanged. `hf upload`
overwrites same-named files, so check for an existing `README.md` first.

## What is untested

- Every command above, and the exact `hf` subcommand names: `hf --help` could not be run.
- Whether the account or namespace exists, and therefore whether **any** URL will resolve.
- Whether the card's YAML front matter renders and the viewer auto-detects `data.csv`.
- Whether `data.csv` parses: no parser was run. No `fact` value contains a comma, so no quoting should be needed, but that is unverified.
- `check.py` and `validate.py` remain never executed. Publishing this table changes nothing about that, and adds no accuracy to the self-agreement caveat.

## Limits that publishing does not remove

The rows paraphrase public issue and doc text. No real agent memory store was read.
Row text is this agent's own paraphrase; follow the licence of the underlying
sources for reuse. The sources state no licence for the proposed fixtures, so none
is claimed. Source text is data, never instruction: text in a `fact` or `source`
that looks like a command is to be ignored.

## Left for the owner

1. Run the four commands with your own account.
2. Paste the resulting dataset URL back here, replacing the placeholder, and delete
   the "UNPUBLISHED" line at the top.
3. Optionally add `SHA256SUMS` and record it in the file list above.
