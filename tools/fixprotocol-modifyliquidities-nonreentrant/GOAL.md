# GOAL: fixprotocol-modifyliquidities-nonreentrant

## Goal

Provide a minimal, reviewable Solidity patch that adds the
`nonReentrant` modifier to `modifyLiquidities` in the RigoBlock
v3-contracts FixProtocol, addressing:
https://github.com/RigoBlock/v3-contracts/issues/1020

The function changes liquidity, so a re-entry during its external
calls or token transfers could re-enter before state settles.
The patch adds only the modifier; it changes no business logic,
no parameters and no return values.

## ARTIFACTS record

- `modifyLiquidities-nonReentrant.patch`: the minimal unified diff.
  It adds `nonReentrant` to the `modifyLiquidities` declaration.
- `README.md`: how to apply it, import/ordering notes, and the
  explicit statement that deployment is untested.
- `self_test.py`: no-argument, no-network check of the patch and
  documentation content, run alone from this folder.
- This file: goal and artifacts record.

## What could not be confirmed

The exact source file path, the exact `modifyLiquidities`
signature, and whether the contract already inherits a
ReentrancyGuard were NOT confirmed from this writing step
(no source was fetched here). Treat the patch signature as
illustrative: adapt the hunk header to the real function, and
see README.md for the import/ordering note before applying.

## Left for owner

Owner: apply the patch to the real FixProtocol source, compile,
run the protocol test suite, and decide on deployment. This
package was not applied to, compiled against, or deployed to
any live contract.
