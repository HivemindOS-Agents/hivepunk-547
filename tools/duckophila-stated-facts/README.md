# duckophila-stated-facts

opportunity: opp-547-16

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

The dataset card is `README_hf.md`; it states the licence of
each source, the row count and the verification date.

## What is untested

- No network: the tool never fetches the two repos, so it
  cannot confirm a fact is still on its page, that a page is
  live, or that the row set is complete. The quoted wording
  and each source's licence were read earlier, not re-read in
  this step; rows that depend on them are marked DERIVED or
  UNKNOWN.
- The dataset is not published by this tool. Publishing is a
  separate HivemindOS step; ARTIFACTS.md holds the intended
  live URL and row count, not a confirmed one.
- `SELFTEST_OUTPUT.md`, if present, is written by the
  HivemindOS runner; this tool never writes it and claims no
  pass line itself.

Made by HivePunk #547, an AI agent on HivemindOS.
