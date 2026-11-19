# stated-facts-check

opportunity: opp-547-15 DuckSpace.org

A small read-only Python checker for row-backed stated-facts
datasets: a CSV with columns `fact_id,topic,claim,source`,
one row per stated fact, each with its exact source URL.
It validates the shape before publishing, e.g. a dataset
compiled only from public DuckSpace pages read today.

## How to run

From this folder:

~~~bash
python3 stated_facts_check.py data.csv
python3 stated_facts_check.py data.csv --allow-domain duckspace.org
python3 stated_facts_check.py data.csv --allow-domain duckspace.org -o report.txt

# Self-test (no arguments, no network, temp files only):
python3 self_test.py
~~~

Checks: all four columns present and non-empty per row;
unique `fact_id`; `source` is a valid `http://`/`https://`
URL with a dotted host; with `--allow-domain` (repeatable)
the source host must equal or be a subdomain of a listed
domain; `claim` is not a bare URL; `topic` contains no URL;
no missing/extra columns or fields; duplicate `claim` text
is a problem. Blank rows are skipped with a stderr note.

Output: a `counts:` line (total / valid / problems), one
`FAIL:` line per problem, or `PASS:` when clean. Exit 0 on
PASS, 1 on any problem or bad/missing/empty input, 2 on
usage error. With `-o`, the report is written to that file
instead of stdout.

`data.csv` in this folder is synthetic sample data only
(example.org sources, not DuckSpace facts) so the tool can
be tried immediately: `python3 stated_facts_check.py data.csv`
should PASS, and with `--allow-domain duckspace.org` it
should FAIL on the example.org hosts, by design.

## Untested

- No network: source URLs are checked for format and host
  only. The tool never fetches a page, so it cannot confirm
  a claim actually appears on its source, that a page is
  live, or that a dataset compiled from pages read today
  is complete or accurate. That editorial check is left
  to the compiler and reviewer.
- Untested against real DuckSpace pages or a real
  published dataset: fixtures and `data.csv` are synthetic.
  Quoted commas/newlines inside CSV fields follow Python
  csv module rules; other dialects are not handled.
- `SELFTEST_OUTPUT.md`, if present later, is written by the
  HivemindOS runner; this tool never writes it, and no
  pass line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
