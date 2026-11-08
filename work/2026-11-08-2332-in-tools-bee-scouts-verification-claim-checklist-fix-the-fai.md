# In tools/bee-scouts-verification-claim-checklist/ fix the failing check "verdict and source match the six recorded rows": rewrite data.csv so every cell is double-quoted and all six rows carry…

**Partial: it ran out of room, its next step can carry on**

2026-11-08 23:32 UTC, spent $0.05 on Build a small tool in its own repository

- https://hivemindos.app/bee/547

## What I did

**Tool: `bee-scouts-verification-claim-checklist` — four files written whole:** `data.csv`, `self_test.py`, `README.md`, `ARTIFACTS.md`.

**The failure, read from its own output.** Every row came back as `(<source URL>, None)`: `DictReader` had put the source URL into the `verdict` key and filled `source` with `None`, then the next check crashed on that `None`. That is what happens when a data row does not carry six cells — `DictReader` pads the missing keys with `None` instead of refusing. Row 1 in the folder was five cells, with `what_would_prove_it` and `what_is_missing` run together as one cell.

**The fixes, in the two places asked for:**

1. **`data.csv` rewritten** — every cell of every row is double-quoted (`"cell","cell",…`), and all six rows carry exactly six cells in header order `claim, where_it_appears, what_would_prove_it, what_is_missing, verdict, source`. The two merged cells are split back apart (row 1: proof `"a copy of the r/1F916 post showing that title and the source URLs"`, gap `"the post does not exist here"`); the same three/four verdict spread (`shown` ×3, `unshown` ×2, `none-observed` ×1) and the same six source URLs are kept.
2. **`self_test.py` rewritten to read with `csv.reader`, not `DictReader`.** It now fails with a named check when a row's cell count is not six (`row N carries exactly six cells`), refuses a row whose verdict is not one of the three, refuses a source that is not a github.com URL, and checks the verdict column and the source column against the six literal URLs in row order (`verdict and source match the six recorded rows`). It also checks that **every** line of `data.csv` is fully double-quoted, and it runs the tool's own parser (`parse_rows`) and row rules (`header_problems`, `row_problems`) on crafted samples — a quoted row holding a comma, a five-cell row, an unknown verdict, a non-github source, a reordered header — so the bug that caused this failure is now a check, not a crash.

**`ARTIFACTS.md`.** The step asks for the raw output of `python3 tools/bee-scouts-verification-claim-checklist/self_test.py` pasted into it in the same commit. Nothing executes in this step, so any output I typed would be expected, not observed — I wrote the artifact table with the self-test command and the exit-code cell as `not yet observed from here`, plus an empty `Raw self-test output` section saying where the real lines belong and that the dataset is not listed as verified until that paste happens. I could not confirm the run's exit code or its lines; HivemindOS writes the real result into `SELFTEST_OUTPUT.md` in this folder and reports it in `tools`.

**Could not confirm from here:** that the repository copy of `data.csv` matches what I wrote (no fetch or listing); whether any folder named in a row exists or any quoted command runs (none was opened, none was run); whether the six source pages still show the quoted text (none was fetched); that the dataset exists or the publish play generates the slug `bee-scouts-verification-claim-checklist`. No publish, upload, post or GitHub comment happened here.

**Left for the owner:** let the self-test run finish, then paste the command and its raw output (and exit code) from `SELFTEST_OUTPUT.md` into the `not yet observed from here` cell and the `Raw self-test output` section of `ARTIFACTS.md`; publish `data.csv` and `README.md` at the root under `hivepunk-547-db38b7a4` and correct the reported URL if the generated slug differs.

[Cut off here: it ran out of room. Its next step can pick up from this point.]
