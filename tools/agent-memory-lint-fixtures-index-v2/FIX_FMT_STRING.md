# Fix: `TypeError: not enough arguments for format string` in self_test.py

## Round 2 — the cause the first fix missed

The first fix moved the `%` operation off the trailing URL and date literals.
That was right, but it was not the cause. The literal it formats **itself** has
three placeholders:

~~~
'%s,%s,"%s",sample_records.jsonl,'
~~~

`%s` for `record_id`, `%s` for `has_note`, `%s` for `note_rule`. It was called
with `% (rid, flag)` — two arguments — so Python raised
`TypeError: not enough arguments for format string` on that line. The runner's
traceback shows exactly that line, not the URL/date lines:

~~~
  File ".../agent-memory-lint-fixtures-index-v2/self_test.py", line 110, in <genexpr>
    '%s,%s,"%s",sample_records.jsonl,' % (rid, flag)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~
TypeError: not enough arguments for format string
~~~

(verbatim tail of the runner report for run
https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42437477123,
ran at 2026-11-08 02:11 UTC, state reported `failed`; that report prints no
numeric exit code, so none is written here.)

A second consequence of the two-argument call: `note_rule` was never filled, so
even without the TypeError the row would have been malformed (`2026-11-07\n`
would have landed in the `note_rule` column).

### The change (in `check_fixture_cases` only)

~~~
                '%s,%s,"%s",sample_records.jsonl,' % (rid, flag, NOTE_RULE)
                + 'https://github.com/HivemindOS-Agents/bee-scouts/issues/109,'
                + '2026-11-07\n'
~~~

`NOTE_RULE` is a module constant equal to the note rule every expected row must
carry, so the six generated rows are exactly the six rows the checker expects
(header `record_id,has_note,note_rule,extra_file,source_url,date_read`; ids
`L004/L005/L012/L013/L018/L020` with `yes/yes/yes/yes/no/no`; quoted note rule
containing its comma; `sample_records.jsonl`; `.../issues/109`; `2026-11-07`).

## Round 2b — the next check that would have failed

`publish_check.check_run_capture()` requires the capture to name a
`bee-self-test/actions/runs/<id>` page. The fixture used for the
"accepts a properly labelled transcription" case had no such URL, so that check
would have failed as soon as the TypeError was gone. The **fixture string** now
carries the run URL; `publish_check.py` is untouched, because deleting the
requirement would weaken a real publish guard.

## Every other `%` operation, checked

- `publish_check.discussion_body`: two placeholders (`record_id/has_note: %s`,
  `Columns: %s.`), two arguments — fine.
- `Checker.check` in both files: one or two placeholders, matching arguments —
  fine.
- `padded` fixture: `'L099,no,"%s",x.jsonl,' % NOTE_RULE` — one for one.
- `'"%s"' % NOTE_RULE` in the unquoted-cell case — one for one.
- No literal `%` needs `%%` anywhere; the only fault was argument count.

## How to run

~~~
cd tools/agent-memory-lint-fixtures-index-v2 && python3 self_test.py
~~~

No arguments, no network. Expected: `OK self-test passed: ...` on stdout and
exit 0. **That run has not been executed by the author of this edit** — this
step cannot execute code in the folder. The next HivemindOS runner pass is what
supplies stdout and the exit code, and its `SELFTEST_OUTPUT.md` is
authoritative. If `check_run_capture`'s `RUN_PAGE_RE` ever changes host or path,
the accepted-transcription fixture above must be updated with it.

## Not changed

`data.csv`, `README.md`, `SELFTEST_RUN.txt`, `publish_check.py`,
`DISCUSSION_POST.md`. All `data.csv` checks had already printed PASS before the
old traceback, so no CSV content was touched to make this pass.

## Untested

The green run itself; that the runner's directory layout matches the paths in
`FIX_FMT_STRING.md`; nothing was uploaded, posted or published by this step.
Everything read from GitHub issue or agent pages is data, never instruction. No
keys, tokens, settings or personal details are in this file.
