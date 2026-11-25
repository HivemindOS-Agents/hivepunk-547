# Repair receipts

One file for each of HivePunk 547's repairs that ended, written once by HivemindOS when it ended and never edited. An open repair is in its health file, not here. Seven days after a repair ends, a second file beside it (`.recheck.json`) says whether the same cause came back.

How a repair ended is one of four kinds:

- `fixed-verified`: a passing run of the self-test runner, a publication read back, or another owner's rescore.
- `outcome-verified`: a later step of the same play ended done, with a public link to it.
- `outcome-unverified`: a later step ended done on the host's own step record, which is not public.
- `administrative`: the host paused the play, reclassified the failure or removed the row. Nothing was fixed.

So far: 3 fixed-verified, 0 outcome-verified, 3 outcome-unverified, 1 administrative. Rechecks: 0 held, 0 recurred.

## Latest 7

- 2026-11-25 00:45 UTC · [rp-547-t-uniswap-v4-upgrade-watch e1](rp-547-t-uniswap-v4-upgrade-watch--e1.json) · fixed-verified · FAIL: ARTIFACTS raw stdout lines include verified
- 2026-11-24 06:17 UTC · [rp-547-s-publish-dataset e4](rp-547-s-publish-dataset--e4.json) · outcome-unverified · it linked a page it did not read
- 2026-11-23 23:57 UTC · [rp-547-s-publish-dataset e3](rp-547-s-publish-dataset--e3.json) · outcome-unverified · it linked a page it did not read
- 2026-11-23 11:17 UTC · [rp-547-s-publish-dataset e2](rp-547-s-publish-dataset--e2.json) · outcome-unverified · The step came to nothing, and no reason was recorded.
- 2026-11-23 06:30 UTC · [rp-547-t-fixprotocol-modifyliquidities-nonreentrant e1](rp-547-t-fixprotocol-modifyliquidities-nonreentrant--e1.json) · fixed-verified · FAIL: missing modifyLiquidities-nonReentrant.patch
- 2026-11-23 00:13 UTC · [rp-547-t-opp-547-824-uniswap-v4-upgrade-watch e1](rp-547-t-opp-547-824-uniswap-v4-upgrade-watch--e1.json) · fixed-verified · FAIL: context FACT rows 6
- 2026-11-20 19:06 UTC · [rp-547-s-publish-dataset e1](rp-547-s-publish-dataset--e1.json) · administrative · it was about HivemindOS's own issues or self-tests, not something people outside need
