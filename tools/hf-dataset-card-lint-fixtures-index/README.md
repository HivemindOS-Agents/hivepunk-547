~~~markdown
# hf-dataset-card-lint-fixtures

This repository contains three tiny folders that serve as **fixtures** for the
[`tools/hf-dataset-card-lint/`](../hf-dataset-card-lint/) linter.

Each folder mimics a minimal dataset that the linter might encounter when
running on a real Hugging Face dataset.  They intentionally contain only the
files required for the linter to exercise its two checks:

* **Row‑count consistency** – whether every CSV row has the same number of
  cells as the header.
* **Closing “what could not be checked” section** – whether the dataset card
  (``README.md``) ends with a dedicated section explaining the linter’s own
  limits.

The three fixture folders are:

- ``clean`` – all rows have the correct number of cells and the card ends with
  a proper closing section.
- ``bad-rows`` – contains a CSV that has one row with two cells and another
  with four cells – both differ from the three‑cell header.
- ``bad-card`` – the CSV is fine, but the card file omits the mandatory
  closing section.

These folders are meant only for unit tests of the linter and **do not**
represent valid Hugging Face datasets.

---

## What could not be checked

No external network access was performed while making this repository.  The
fixture files were written by hand using the minimal structure required by the
linter; none of them were generated or altered by any script that might talk
to the internet.  Consequently, this README ends with a list of checks that
could not be performed programmatically.
~~~
