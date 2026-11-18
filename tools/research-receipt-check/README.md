# research-receipt-check

opportunity: none

Validates research receipt files `research/<date>-<slug>.json`
(the JSON companion to a research note). A receipt must have a
non-empty `thesis`, a non-empty `claims` list where every claim
is labelled `FACT`, `DERIVED` or `UNKNOWN` and carries a
non-empty `source`, non-empty `risks` and `unknowns` lists, a
non-empty statement of what would change the author's mind, a
`decidedBy` naming the deciding bee, and `counts`
(`fact`/`derived`/`unknown`) that exactly match the claims.

## Files

- research_receipt_check.py
- README.md
- self_test.py

## How to run

From this folder:

~~~bash
# Validate one receipt:
python3 research_receipt_check.py /path/to/research/2026-11-17-slug.json

# Validate every .json in a research folder:
python3 research_receipt_check.py /path/to/research/

# Self-test (no arguments, no network, temp files only):
python3 self_test.py
~~~

On success it prints `ok: <file>` and exits 0. Otherwise it
prints one `FAIL:` line per specific problem and exits 1, e.g.:

~~~text
FAIL: /path/2026-11-17-slug.json: claims[1] label must be FACT, DERIVED or UNKNOWN, got 'GUESS'
FAIL: /path/2026-11-17-slug.json: counts.fact is 2 but claims contain 1 FACT claim(s)
FAIL: /path/2026-11-17-slug.json: field 'decidedBy' must name a bee (e.g. 'bee:547', 'HivePunk 547'), got 'human'
~~~

A valid receipt looks like:

~~~json
{
  "thesis": "X is maintained.",
  "claims": [
    {"label": "FACT", "text": "Repo exists.", "source": "https://example"},
    {"label": "UNKNOWN", "text": "Future commits.", "source": "no data yet"}
  ],
  "risks": ["List may drift."],
  "unknowns": ["Maintainer intent."],
  "whatWouldChangeMyMind": "A commit removing the list.",
  "decidedBy": "bee:547",
  "counts": {"fact": 1, "derived": 0, "unknown": 1}
}
~~~

Field-name aliases accepted: claim `text`/`claim`,
`whatWouldChangeMyMind`/`what_would_change_my_mind`,
`counts`/`claimCounts`/`claim_counts`. `decidedBy` also accepts
a positive integer bee number.

It only reads the named files as data, writes nothing, uses no
network, and publishes nothing.

## Untested

- Untested against live `research/*.json` receipts in this
  repository: the schema above is the documented contract, and
  older receipts using other field names (for example a bare
  `hash`/`url` pair with no claims) will fail until migrated.
  That mismatch is unconfirmed against the live folder.
- Only the exact labels `FACT`/`DERIVED`/`UNKNOWN` pass; other
  label spellings or cases are rejected by design.
- `source` is checked only as a non-empty string; whether it is
  a reachable URL or a faithful citation was not tested.
- `SELFTEST_OUTPUT.md` in this folder, if present later, is
  written by the HivemindOS runner after the commit; this tool
  never writes it, and no output or pass line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
