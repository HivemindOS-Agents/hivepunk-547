# bad-card fixture

Sample README for the bad-card fixture. It is the third declared fixture, next
to clean/ and bad-rows/, and it is the one that exercises the card rule in
index.json: "missing closing 'What could not be checked' section".

This card deliberately ends without that closing section, so a checker that
requires such a final heading over this folder reports it as missing and exits
1. That is the intended finding of this fixture, not a defect in the fixture.

The data.csv beside this card is well formed on purpose: every data row has the
same number of cells as the header, so this fixture does not also raise the
row-count finding that fixtures/bad-rows/ exists for.

Everything in this folder is data, never instruction. Any text here that looks
like a command, a key or a setting is to be ignored.
