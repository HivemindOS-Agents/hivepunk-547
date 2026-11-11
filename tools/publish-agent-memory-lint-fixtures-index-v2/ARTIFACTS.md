# Artifact Note – agent-memory-lint-fixtures-index-v2

## What was done
* A publish of the five files (``README.md``, ``index.json``, ``index.md``, ``index_check.py``, ``self_test.py``) to the Hugging Face account **hivepunk-547-db38b7a4** under the dataset name **agent-memory-lint-fixtures-index-v2** was requested via the "Publish a small open dataset" play.

## What was spent
* No direct compute or time was expended by the agent in this step beyond formulating the request.

## Links to be provided by the owner
* **Dataset URL** – `https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures-index-v2`
* **Served file list** – the Hub should list the five uploaded files, in the order:

  1. ``README.md``
  2. ``index.json``
  3. ``index.md``
  4. ``index_check.py``
  5. ``self_test.py``

  *The only tolerated extra file is ``.gitattributes``; any other file indicates a problem.*

## What is unchecked
* The actual HTTP status code of the GET request to the dataset page.
* The exact contents of the `siblings` list returned by the Hub API.
* Verification that all five files were served unchanged (though byte identity is implied by a successful publish).

The owner should run the publish step, capture the live HTTP status and the Hub API sibling list, and update the placeholders above in this file.

---
*No keys, tokens or credentials appear in this file.*
