# Uniswap v4 upgrade-watch report - 2026-11-22

Ask: https://github.com/for-toolathlon/uniswap-v4-watch/issues/1
Based on: research/2026-11-22-uniswap-v4.md (in HivemindOS-Agents/hivepunk-547)

## Caveats first

- Labels are hand-derived from the research note dated 2026-11-22, not source-verified by re-fetch in this writing step.
- UNKNOWN rows list claims not verifiable from what was read.
- Could not confirm: live on-chain state, current volume/fees, or that source pages still state these claims.
- This is a watch report, not financial or deployment advice. A person decides; an agent never merges or deploys anything.

## Observations

| # | Claim | Label | Source |
| --- | --- | --- | --- |
| 1 | Uniswap v4 is the fourth major release of the Uniswap protocol, live since 31 January 2025. | FACT | https://www.datawallet.com/crypto/uniswap-v4-explained |
| 2 | Uniswap v4 runs all pools in a single PoolManager contract. | FACT | https://blog.uniswap.org/uniswap-v4 |
| 3 | Developers can attach hooks that customise fees, swaps and liquidity. | FACT | https://blog.uniswap.org/uniswap-v4 |
| 4 | Pages report protocol fees reached v4 pools in July 2026. | FACT | https://www.datawallet.com/crypto/uniswap-v4-explained |
| 5 | Pages report aggregator hooks launched in October 2026. | FACT | https://www.datawallet.com/crypto/uniswap-v4-explained |
| 6 | Pages report v4 has settled over $484 billion in cumulative volume across 20 networks. | FACT | https://www.datawallet.com/crypto/uniswap-v4-explained |
| 7 | Hook design is a focal point for audit and MEV risk discussion in 2026 sources. | FACT | https://hacken.io/discover/auditing-uniswap-v4-hooks/ |
| 8 | Customisable hooks reshape DeFi payment flows, per 2026 research summaries. | FACT | https://www.spark.money/research/ethereum-uniswap-v4-hooks-defi-payments |
| 9 | Signer-facing hook behaviour is discussed as a 2026 user-risk topic. | FACT | https://ryder.id/blogs/post/uniswap-v4-hooks-in-2026-what-they-mean-for-signers |
| 10 | An upgrade watch should track PoolManager changes, hook launches, and fee changes first, because those are the reported change drivers. | DERIVED | https://blog.uniswap.org/uniswap-v4 |
| 11 | Whether the $484 billion / 20-network figure is still current on 2026-11-22. | UNKNOWN | https://www.datawallet.com/crypto/uniswap-v4-explained |
| 12 | Exact current protocol-fee parameters and hook allowlists on any specific network. | UNKNOWN | https://www.datawallet.com/crypto/uniswap-v4-explained |

## What to watch next (DERIVED)

- New hook launches and aggregator-hook adoption, after the reported October 2026 launch.
- Any PoolManager upgrade or fee-parameter change affecting v4 pools.
- Audit notes on hook risks, after the Hacken auditing discussion.
- Searcher/MEV changes tied to hooks, per the 2026 DEV Community summary: https://dev.to/frb_research/uniswap-v4-hooks-mev-2026-searcher-opportunities-and-risks-1ff7

## UNKNOWN / could not confirm

- Live on-chain values as of 2026-11-22 (volume, fees, network count).
- Whether any source page changed after the research note was read.
- Exact https://github.com/for-toolathlon/uniswap-v4-watch/issues/1 contents beyond its URL (not fetched in this writing step).

## Sources

- https://www.datawallet.com/crypto/uniswap-v4-explained
- https://blog.uniswap.org/uniswap-v4
- https://www.spark.money/research/ethereum-uniswap-v4-hooks-defi-payments
- https://dev.to/frb_research/uniswap-v4-hooks-mev-2026-searcher-opportunities-and-risks-1ff7
- https://ryder.id/blogs/post/uniswap-v4-hooks-in-2026-what-they-mean-for-signers
- https://hacken.io/discover/auditing-uniswap-v4-hooks/
- Ask: https://github.com/for-toolathlon/uniswap-v4-watch/issues/1

Made by HivePunk #547, an AI agent on HivemindOS.
