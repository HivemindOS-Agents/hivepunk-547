# Agent Memory Viewer Readback Log

This tool runs a self-test that imports the viewer_readback module and
performs the four expected HTTP calls using a fixture map (URL →
{http_status, body}). The self-test outputs the result of each call and
signals success only when all four calls satisfy the unlock rules.

## Self-test watched
self-test watched: pass, all checks (run 2026-11-04)
