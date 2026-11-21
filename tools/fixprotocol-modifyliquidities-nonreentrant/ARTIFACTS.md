# fixprotocol-modifyliquidities-nonreentrant: artifact record

Folder-local record only. Nothing recorded here was run by this
writing step, and this file is not one of self_test.py's inputs.

## The exact command

~~~bash
python3 self_test.py
~~~

Run from inside this folder, with no arguments and no network.
Folder: tools/fixprotocol-modifyliquidities-nonreentrant/

## Where its raw output goes

The HivemindOS runner runs that command after every commit. It
writes each run's result into SELFTEST_OUTPUT.md in this folder
and reports the state and the last lines it printed in the tools
listing, with the runner page for the run. This folder's own
entry point writes no pass line, no run log and no captured
output.

The raw output for the current commit is NOT pasted here: it had
not been produced when this file was written, and nothing this
folder writes has been run.

## Slot for the runner's raw output (paste, never invent)

~~~text
(paste the runner's raw SELFTEST_OUTPUT.md text here, unedited)
~~~

## What is in this folder

- modifyLiquidities-nonReentrant.patch - one-hunk UNTESTED diff.
- README.md - apply steps, import/ordering note, untested wording.
- GOAL.md - goal, artifacts record, local check, unconfirmed items.
- ARTIFACTS.md - this file.
- self_test.py - the content checks; no arguments, no network.

## What was confirmed, and what was not

- NOT confirmed: that `python3 self_test.py` exits 0. No run has
  been seen from this writing step. SELFTEST_OUTPUT.md, written
  by the runner, is the only place a result is recorded.
- NOT confirmed: that the patch applies to, compiles against, or
  passes tests on the real RigoBlock v3-contracts source. The
  file path and the parameter list in the diff are illustrative.
- Confirmed by reading this folder only: the five files exist,
  and the patch carries the issue link, the nonReentrant modifier
  on the modifyLiquidities declaration, and an UNTESTED marker.
- The self-test does not read this file, so nothing above is
  checked by it.

## Left for owner

Owner: let the HivemindOS runner run the command above after this
commit, paste its raw output into the slot, then apply the patch
to the real source, compile and test before deciding anything
about deployment.
