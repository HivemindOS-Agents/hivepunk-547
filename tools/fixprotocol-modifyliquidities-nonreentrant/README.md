# fixprotocol-modifyliquidities-nonreentrant

opportunity: opp-547-46

Minimal patch adding `nonReentrant` to `modifyLiquidities`
(RigoBlock v3-contracts, issue
https://github.com/RigoBlock/v3-contracts/issues/1020).

## Files

- `modifyLiquidities-nonReentrant.patch` - unified diff, one hunk
  with a single -/+ line (a short header above it is skipped by
  GNU patch).
- `GOAL.md` - goal, artifacts record, local check.
- `ARTIFACTS.md` - the exact self-test command and the slot where
  the runner's raw output is pasted.
- `self_test.py` - content checks, no network, no arguments.

## How to apply (owner, on the real source)

~~~bash
# from a checkout of RigoBlock/v3-contracts, after review:
patch -p1 < modifyLiquidities-nonReentrant.patch
~~~

Then adapt the hunk to the real file/function if the context
lines differ, compile, and run the protocol tests.

## Import / ordering note

- `nonReentrant` is not a Solidity builtin. The contract must
already inherit a guard that defines it (for example
OpenZeppelin `ReentrancyGuard`, imported and inherited as
`contract FixProtocol is ReentrancyGuard { ... }`). If it does
not, add that import/inheritance first; the modifier alone
will not compile. If it already does, no import change is
needed - add only the modifier, as in the patch. Whether the
real FixProtocol already inherits a guard was not confirmed
here: the source was not read.
- Modifier ordering: Solidity runs modifiers left to right.
Put `nonReentrant` last, after access/validation modifiers
(for example `onlyOwner`), so the guard lock is acquired
immediately before the function body and released on exit,
and rejected callers never take the lock.
- Keep checks-effects-interactions inside the body: update
liquidity state before external calls where the code allows it.
The modifier is defence in depth, not a substitute for that.

## Untested - read before deploying

UNTESTED DEPLOYMENT: this patch has NOT been compiled against
the real FixProtocol source, has NOT been run through the
protocol test suite, and has NOT been deployed anywhere. The
exact file path and function signature were not confirmed from
this writing step, so the diff is minimal and illustrative.
Do not deploy it without applying it to the real source,
compiling, and testing first. A person decides; an agent never
merges or deploys anything.

## Self-test

~~~bash
python3 self_test.py
~~~

No arguments, no network, run alone from this folder. It checks
the patch text and this README/GOAL wording and exits 0 only
when every check passes. It does not read ARTIFACTS.md.

The authoritative run result is SELFTEST_OUTPUT.md, written by
the HivemindOS runner after commit; this folder writes no pass
line itself. ARTIFACTS.md records the exact command and holds
the slot for that raw output.

Made by HivePunk #547, an AI agent on HivemindOS.
