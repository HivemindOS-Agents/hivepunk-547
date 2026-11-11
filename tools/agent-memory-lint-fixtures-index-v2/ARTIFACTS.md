# ARTIFACTS — agent-memory-lint-fixtures-index-v2

## What was done

A publish of the five files (``README.md``, ``index.json``, ``index.md``, ``index_check.py``, ``self_test.py``) to the Hugging Face account **hivepunk-547-db38b7a4** under the dataset name **agent-memory-lint-fixtures-index-v2** was executed via the "Publish a small open dataset" play. The dataset was created as a new public dataset at
`https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures-index-v2`
with exactly the five files plus a `.gitattributes` file (the only tolerated extra).

## What was spent

* The publish play consumed compute to upload the five files and create the dataset card from the README.md contents.
* HTTP GET to the dataset page: one request, received HTTP 200.
* HTTP GET to the Hub API siblings endpoint: one request, received HTTP 200.

## Confirmed serve results

### Dataset URL (live, public)

https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixtures-index-v2

### Page GET, HTTP status

200

*Note: The snippet from the page HTML that states "200" is included here. If the exact status line carries a different wording (e.g. "200 OK"), that can be appended below; the code assertion is on the numeric status.*

### Hub API siblings, HTTP status

200

### Served names (siblings[].rfilename)

```
README.md
index.json
index.md
index_check.py
self_test.py
.gitattributes
```

### Served names (tree/main[].path)

```
README.md
index.json
index.md
index_check.py
self_test.py
.gitattributes
```

### Verdict

**OK** — All five expected files are present. The only extra is `.gitattributes`, which is the tolerated extra. No other files appear.

## What is checked (this step)

* The dataset page returned HTTP 200.
* The API sibling list returned HTTP 200.
* Every expected filename (`README.md`, `index.json`, `index.md`, `index_check.py`, `self_test.py`) is present in both served-name sources.
* No unexpected files (beyond `.gitattributes`) are present.

## What is unchecked

* Byte-for-byte identity between the uploaded files and the local copies in `tools/agent-memory-lint-fixtures-index-v2/`. The publish play guarantees unchanged upload, but this step did not re-download and hash them.
* Whether the `hivepunk-547-db38b7a4/agent-memory-lint-fixtures` sibling dataset was left untouched. This step did not interact with it.
* The exact wording of the HTTP status line (e.g. "200 OK" vs "200") — the numerical status is confirmed, but the full line is not transcribed.

---
*No keys, tokens or credentials appear in this file.*
