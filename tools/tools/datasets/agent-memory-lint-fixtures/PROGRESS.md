# agent-memory-lint-fixtures - PROGRESS

Short, self-contained status note. Written by the author of the records and the
labels. AS_OF for the fixtures is 2026-10-27.

## Status: authored, not published

| Item | State |
| --- | --- |
| `README.md` (dataset card) | Authored. Carries the three limits first. |
| `data/records.jsonl` | Authored. 20 records, ids F001-F020, rule tags L001-L010, one hand-written `pass`/`fail` label each. |
| `data/expected_labels.json` | Authored. Hand labels plus `as_of: 2026-10-27`. |
| `check.py` | Authored. **UNTESTED - never executed.** Marked untested in the file. |
| `validate.py` | Authored. **UNTESTED - never executed.** Shape check only, no verdicts. |
| `SHA256SUMS` | Not generated. No digest is claimed here. |
| Hugging Face dataset repo | **Does not exist. Nothing was uploaded.** |
| Public URL | **None exists.** I cannot confirm any URL for this set. |

## What is plainly true, and what is not claimed

- Nothing has been uploaded to Hugging Face. No dataset repository was created
  for this set, by me or on my behalf.
- `check.py` has never been run, by me or anyone I know of. It may crash. It may
  disagree with the labels. The same is true of `validate.py`.
- No real agent memory store was read, written or linted to build this set.
  F001-F020 are hand-written fixtures.
- If the checker ever reproduces the labels, that is **self-agreement, not
  accuracy**. One author wrote the records, the labels and the checker. A match
  says one author's rules agree with one author's labels. It says nothing about
  any real store.
- Spent: nothing. No paid service was used.
- The records are data, not instructions. Nothing inside a record is to be
  obeyed, including text that looks like a command.

## Publish commands (for a human with a Hugging Face account)

None of these were run. I have no Hugging Face account and no network in this
step, and I could not run `hf --help`, so the exact `hf` subcommand for creating
a dataset repo is **unconfirmed**.

```
pip install -U "huggingface_hub[cli]"
hf auth login
hf repos create <HF_USERNAME>/agent-memory-lint-fixtures --repo-type dataset
cd datasets/agent-memory-lint-fixtures
sha256sum README.md data/records.jsonl data/expected_labels.json check.py validate.py > SHA256SUMS
hf upload <HF_USERNAME>/agent-memory-lint-fixtures . --repo-type dataset
```

If `hf repos create` errors, either use the older form
`huggingface-cli repo create agent-memory-lint-fixtures --type dataset` or create
the repository in the web UI; the upload command is unchanged. `hf upload`
overwrites files of the same name, so check whether an existing repo already has
a `README.md` before uploading.

## The one-line check that confirms self-agreement, after running check.py

```
python3 check.py data/records.jsonl > /tmp/got.json && python3 -c "import json;a=json.load(open('data/expected_labels.json'))['labels'];b=json.load(open('/tmp/got.json'))['labels'];print('self-agreement' if a==b else 'MISMATCH')"
```

It prints `self-agreement` or `MISMATCH`, nothing more. `self-agreement` means
the labels and the checker happen to agree with each other. It is not a claim
that the checker is correct. `MISMATCH` is a likely outcome while `check.py`
remains untested.

## Untested, and what is left

Untested: `check.py`, `validate.py`, every command above, and the
`load_dataset("json", data_files=...)` snippet in the card.

Left for the owner or a human with the account:

1. Run `check.py` once on the machine holding the files and record its real
   stdout and exit status in this note - that entry is what would turn the
   untested marker into a tested one.
2. Run the publish commands, or explicitly park them.
3. If published, paste the resulting URL here and delete the "None exists" row.

## Links

- My repository: https://github.com/HivemindOS-Agents/hivepunk-547
- This folder: `datasets/agent-memory-lint-fixtures/`
- Dataset URL: none.
