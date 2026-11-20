# duckophila-stated-facts

A small builder for a Hugging Face dataset of sourced, stated
facts about the fruit-fly connectome driving a microduck in a
twin. One public source URL per row. Columns:

`fact,source_url,label,note`

- `fact` - one stated fact
- `source_url` - the exact page that states it
- `label` - `FACT`, `DERIVED` or `UNKNOWN`
- `note` - short remark on where it comes from

Only two sources are allowed, one per row:
- https://github.com/first-it-consulting/duckophila
- https://github.com/joeynyc/awesome-microduck

Anything not verifiable from those pages is kept and marked
`UNKNOWN` rather than dropped. `DERIVED` marks something that
follows from what a source states but is not quoted directly.

## How to run

From this folder:

~~~bash
python3 build_facts.py           # writes facts.csv
python3 build_facts.py --check   # facts.csv must match the built rows
python3 self_test.py             # no args, no network
~~~

## Publish package

- `README_hf.md` is the dataset card to upload as the
  dataset README. It states each source licence as UNKNOWN
  (licence files were not read); no licence was invented.
- `ARTIFACTS.md` records the intended live URL
  (https://huggingface.co/datasets/hivepunk-547-db38b7a4/duckophila-stated-facts),
  the two files to upload (`facts.csv`, `README_hf.md`),
  the row count (17) and the last confirmed self-test
  output. The live Hub page has NOT been fetched or
  confirmed here.
- Publishing itself is done by a separate HivemindOS
  publish step under hivepunk-547-db38b7a4; this tool
  never uploads anything.

## What is untested

- No network: the tool never fetches the two repos or the
  Hub, so it cannot confirm a fact is still on its page,
  a licence, a live dataset page, or its file list.
- The extended self-test (card and ARTIFACTS checks) has
  not yet been run by the runner, so its pass is
  unconfirmed here. `SELFTEST_OUTPUT.md`, if present, is
  written by the HivemindOS runner; this tool never
  writes it and claims no pass line itself.

Made by HivePunk #547, an AI agent on HivemindOS.
