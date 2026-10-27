# Draft the exact unified diff for a small, additive edit to huggingface/hub-docs `datasetcard.md` (the source of https://huggingface.co/docs/hub/datasets-cards): add an optional `source:` provenance key (origin, contributors, labels_by) to the example YAML front matter, with the surrounding before/after context. Return the diff plus commit message and PR description text; do not open or merge anything.

**Done**

2026-10-27 15:09 UTC, spent $0.02 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/547

```json
{
  "id": "msg_011CgSxFZYoxpVm7Mr3AQXzC",
  "object": "chat.completion",
  "created": 1793113761,
  "model": "claude-haiku-5-5",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "I can't see the repository's current contents from here, so I can't guarantee the exact line numbers or surrounding text in `datasetcard.md` match the live file. Below is a diff built against the example front matter as I understand it (the standard `license`, `task_categories`, `language`, `size_categories`, `pretty_name` block). Before using it, run `git apply --check` against your checkout and adjust the hunk header and context lines to match.\n\n```diff\n--- a/datasetcard.md\n+++ b/datasetcard.md\n@@ -12,6 +12,19 @@ language:\n - en\n size_categories:\n - 1K<n<10K\n pretty_name: My Dataset\n+# Optional: provenance of the data. All subkeys are optional.\n+source:\n+  origin: \"Where the raw data came from (e.g. a URL, publication, or internal system)\"\n+  contributors:\n+  - \"Person or organization that collected, created, or curated the data\"\n+  labels_by: \"Who or what produced the labels (e.g. human annotators, an LLM, a rule-based process)\"\n ---\n \n # Dataset Card for My Dataset\n```\n\n**Commit message**\n\n```\ndocs(datasetcard): document optional `source` provenance key\n\nAdd an optional `source` block to the dataset card YAML front matter\nexample, with three optional subkeys:\n\n- origin: where the raw data came from\n- contributors: people or organizations that collected or curated it\n- labels_by: who or what produced the labels\n\nThe key is additive and optional; existing dataset cards remain valid.\n```\n\n**PR description**\n\n```\n## Summary\n\nAdds an optional `source` key to the dataset card front matter example\nin `datasetcard.md`, documenting data provenance in three optional\nsubfields: `origin`, `contributors`, and `labels_by`.\n\n## Motivation\n\nDataset cards currently have no standard place in the front matter to\nrecord where data originated or who labeled it. Users increasingly need\nthis for licensing review, bias analysis, and reproducibility. Making it\npart of the documented schema lets tooling read it consistently.\n\n## Changes\n\n- Adds a `source` block to the example YAML front matter only.\n- No existing keys are renamed or removed.\n\n## Notes for reviewers\n\n- Purely additive and optional; no change to required fields.\n- If the hub's metadata validator enforces a fixed key set, that\n  validator would need a matching update before this key is accepted\n  as valid. Worth confirming with maintain"
      },
      "finish_reason": "length"
    }
  ],
  "usage": {
    "prompt_tokens": 141,
    "completion_tokens": 800,
    "total_tokens": 941
  }
}
```
