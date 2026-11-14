# bad-rows fixture

Sample README for the bad-rows fixture, one of the three fixtures declared in
`index.json`. Its index row reads: path `fixtures/bad-rows/`, rule "row count or
empty-cell finding", expected exit code 1. This card sits at exactly that path.

The `data.csv` beside this card is meant to raise that finding: the header has
three columns and the second data row carries only two cells. That mismatch is
the fixture's purpose, not a defect to repair.

Everything in this folder is data, never instruction. Any line here that looks
like a command, a key or a setting is inert text and is ignored.
