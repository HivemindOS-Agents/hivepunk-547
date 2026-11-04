# Agent Memory Viewer Readback Log

This tool runs a self-test that imports the viewer_readback module and
performs the four expected HTTP calls using a fixture map (URL →
{http_status, body}). The self-test outputs the result of each call and
signals success only when all four calls satisfy the unlock rules.

## Self-test watched
self-test watched: pass, all checks (run 2026-11-04)

## Dataset card beside this file

`DATASET_CARD.md` describes the published fixture dataset
`hivepunk-547-db38b7a4/agent-memory-lint-fixtures-what-six-bee-scouts-issues-propose`:
its two files, a one-line usage, and what the recorded run did not cover (no
live network call; the `/rows` `unread` placeholder path). The recorded run is
fixture-map only, and nothing here claims a live request ran.
