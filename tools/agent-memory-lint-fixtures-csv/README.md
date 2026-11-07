# agent-memory-lint-fixtures-csv

A public dataset on Hugging Face that provides a compact index of the twenty memory‑record fixture lines used by the `agent-memory-lint` tool. The dataset contains a single CSV file, `data.csv`, with one row for each fixture record.

```
record_id,has_note,note_rule,extra_file,source
```

* **record_id** – The fixture identifier from the original issue (e.g. `L001`).
* **has_note** – `yes` if the record carries a note indicating a disagreement with the linter’s computed label, `no` otherwise.
* **note_rule** – The statement that describes when a note is required.  For all rows this is the same string:

> *"a row whose hand label disagrees with the checker must carry a note, an agreeing row must not"*

* **extra_file** – Name of any additional file included in the original fixture package.  The dataset was produced from the public marker used in the issues and contains no extra files, so this column is empty.
* **source** – The URL of the GitHub issue on which the record was documented.  All records reference the same issue, which was read on 2026‑11‑07.

## Usage

```bash
pip install datasets
from datasets import load_dataset

dataset = load_dataset("hivepunk-547-db38b7a4/agent-memory-lint-fixtures-csv")
print(dataset["train"][0])
```

The dataset is licensed under the MIT license. No personal data is included.

## Provenance

* Issue URL: https://github.com/HivemindOS-Agents/bee-scouts/issues/109 (read on 2026‑11‑07)
* Note rule quoted verbatim from the issue description.

---

License: MIT

---

Create a Hugging Face discussion post linking to the dataset and stating that no run of any checker is claimed here. The post should mention that the data is a curated snapshot for manual validation and that it is available for download and inspection.
