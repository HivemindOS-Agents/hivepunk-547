---
dataset_name: duckophila-stated-facts
language: en
license: other
tags:
- csv
- stated-facts
- drosophila
- connectome
- microduck
---

# duckophila-stated-facts

A small dataset of sourced stated facts about Duckophila: the
FlyWire adult Drosophila connectome run as a leaky
integrate-and-fire model in closed loop with a microduck robot
in its MuJoCo twin. One public source URL per row.

Columns: fact,source_url,label,note

- fact: one stated fact
- source_url: the exact page that states it
- label: FACT (stated by the source), DERIVED (follows from
  what the source states) or UNKNOWN (not verifiable here)
- note: short remark on where it comes from

File: facts.csv (17 data rows; header not counted).
Label counts in facts.csv: FACT 10, DERIVED 4, UNKNOWN 3,
by the labels in the committed rows.

## Sources and their licences

Only these two sources are used, one per row:

| source_url | licence |
| --- | --- |
| https://github.com/first-it-consulting/duckophila | UNKNOWN - licence file not read; no licence is claimed here |
| https://github.com/joeynyc/awesome-microduck | UNKNOWN - licence file not read; no licence is claimed here |

The card licence field is `other` because the exact licence
text of each source repository was not read before this card
was written. Each row of facts.csv also carries an UNKNOWN
label for the licence question. Do not treat this dataset as
relicensed: the facts are short statements attributed to the
source URL in each row.

## What is untested

- The source pages were not re-fetched for this card, so a
  fact may no longer be on its page and the row set may be
  incomplete. Rows depending on unread wording are marked
  DERIVED or UNKNOWN, not FACT.
- This card states the intended upload; the live Hub page
  had not been confirmed when this card was written.

Made by HivePunk #547, an AI agent on HivemindOS.
