# Self-test of bee-scouts-verification-claim-checklist

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-08T22:44:21Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42531701800

What it printed (what failed first, then its last lines):

~~~
FAIL verdict and source match the six recorded rows -- [('https://github.com/HivemindOS-Agents/bee-scouts/issues/122', None), ('https://github.com/LiamVisionary/bee-scouts/issues/32', None), ('https:/
FAIL every verdict is shown, unshown or none-observed
Traceback (most recent call last):
             ~~^^
  File "[redacted], line 99, in main
    c.check(all(SOURCE_RE.match(r['source']) for r in rows),
            ^^^
  File "[redacted], line 99, in <genexpr>
    c.check(all(SOURCE_RE.match(r['source']) for r in rows),
                ~~^^^^^^^^^^^^^
TypeError: expected string or bytes-like object, got 'NoneType'
~~~
