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
  A short comment header (issue link, UNTESTED marker, apply
  command), then one hunk replacing the `modifyLiquidities`
  declaration line with the same line plus `external
  nonReentrant`.
- `README.md`: how to apply it, the import/ordering note, and the
  explicit statement that the patch is untested.
- `ARTIFACTS.md`: the exact self-test command, where its raw
  output is written, and the empty slot for pasting it.
  Note: ARTIFACTS.md could not fit in the 4-file limit of the
  commit that added the patch; its latest-failure slot update
  is pending owner paste of the runner raw output below.
- `self_test.py`: no-argument, no-network check of the patch and
  documentation content, run alone from this folder.
- This file: goal and artifacts record.

## Latest runner failure (exact mismatch fixed here)

State: failed, ranAt: 2026-11-22 01:37 UTC, run:
https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44972300158
Output: FAIL: missing modifyLiquidities-nonReentrant.patch

Previous failure also: ranAt 2026-11-21 22:23 UTC, run 44956526668,
same output. The prior commit claimed to add the patch but its
file list contained only self_test.py, README.md and GOAL.md,
so the runner still saw it missing. This commit adds exactly
that file: modifyLiquidities-nonReentrant.patch, matching the
filename self_test.py opens. self_test.py and README.md wording
were not changed to make the check pass.

## Local check

The intended check is exactly:

~~~bash
python3 self_test.py
~~~

run with no arguments, no network, from inside this folder alone.
Raw command: python3 self_test.py - exit code: NOT confirmed from
this writing step (no run was performed here, so no exit code or
output is claimed) - output: NOT confirmed. Its authoritative
result is written by the HivemindOS runner into SELFTEST_OUTPUT.md.
This folder writes no pass line itself and asserts no result: the
runner's result is the only evidence that counts.

## What could not be confirmed

The exact source file path, the exact `modifyLiquidities`
signature, and whether the contract already inherits a
ReentrancyGuard were NOT confirmed from this writing step (no
source was fetched here). Treat the patch signature as
illustrative: adapt the hunk header to the real function, and
see README.md for the import/ordering note before applying.
Compilation against real FixProtocol source is untested.

Also NOT confirmed here: that `python3 self_test.py` exits 0.
No run was seen from this writing step, so no raw output is
pasted in ARTIFACTS.md; the runner's SELFTEST_OUTPUT.md is the
only place a result is recorded. No passing standalone runner
output has been seen yet.

## Left for owner

Owner: let the runner run the check above from this folder alone,
paste its raw output into ARTIFACTS.md, then apply the patch to
the real FixProtocol source, compile, run the protocol test suite,
and decide on deployment. This package was not applied to,
compiled against, or deployed to any live contract.
