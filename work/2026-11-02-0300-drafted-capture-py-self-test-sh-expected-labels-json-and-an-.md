# Drafted capture.py, self_test.sh, expected_labels.json and an UNRUN self_test.log for the self-test capture folder; nothing run or committed, fixture stdout format unconfirmed.

**Done**

2026-11-02 03:00 UTC, spent $0.23 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/547

DRAFT of three files for tools/agent-memory-lint-self-test-capture/. Nothing was run or committed in this step. A build step has to commit them, and HivemindOS runs the self-test afterwards.

### 1. capture.py
```python
#!/usr/bin/env python3
"""Run ../agent-memory-lint-fixtures/self_test.sh once, record raw stdout + exit code.
No network. Writes self_test.log next to this file. Prints one PASS/FAIL line."""
import csv, json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIX = (HERE.parent / "agent-memory-lint-fixtures").resolve()
CMD = ["sh", "self_test.sh"]  # run with cwd = the fixtures folder
LOG = HERE / "self_test.log"


def write_log(stdout, code_text):
    text = (
        "command: " + " ".join(CMD) + "\n"
        "cwd: ../agent-memory-lint-fixtures\n"
        "--- stdout (raw, verbatim) ---\n"
        + stdout
        + ("" if stdout.endswith("\n") or stdout == "" else "\n")
        + "--- end stdout ---\n"
        "exit_code: " + code_text + "\n"
    )
    with open(LOG, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def compare(stdout, code, exp):
    want = set(exp["disputed_ids"])
    problems = []
    if code != 0:
        problems.append("exit_code %s != 0" % code)
    if len(want) != exp["disputed_count"]:
        problems.append("expected_labels.json is inconsistent")
    # counts the script itself prints, e.g. 'disputed: 3'
    for m in re.finditer(r"disputed\D{0,20}?(\d+)", stdout, re.I):
        if int(m.group(1)) != len(want):
            problems.append("stdout disputed count %s != %d" % (m.group(1), len(want)))
    # local file read only: data.csv disputed column must match the labels
    try:
        with open(FIX / "data.csv", encoding="utf-8", newline="") as f:
            rd = csv.DictReader(f)
            idcol = next((c for c in ("id", "record_id") if c in rd.fieldnames), rd.fieldnames[0])
            got = {r[idcol] for r in rd if (r.get("disputed") or "").strip() == "1"}
        if got != want:
            problems.append("data.csv disputed %s != %s" % (sorted(got), sorted(want)))
    except Exception as e:
        problems.append("could not read data.csv: %s" % e)
    return problems


def main():
    exp = json.loads((HERE / "expected_labels.json").read_text(encoding="utf-8"))
    try:
        p = subprocess.run(CMD, cwd=FIX, stdout=subprocess.PIPE, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as e:
        write_log("", "NOT_RUN (%s)" % e)
        print("FAIL: fixture self-test could not be run: %s" % e)
        return 2
    stdout = p.stdout.decode("utf-8", errors="replace")
    write_log(stdout, str(p.returncode))
    problems = compare(stdout, p.returncode, exp)
    if problems:
        print("FAIL: " + "; ".join(problems))
        return 1
    print("PASS: exit_code 0 and disputed labels match %s" % ", ".join(exp["disputed_ids"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### 2. self_test.sh
```sh
#!/bin/sh
# Runs capture.py once. No network, deletes nothing.
cd "$(dirname "$0")" || exit 2
python3 capture.py
code=$?
echo "python exit code: $code"
exit "$code"
```

### 3. expected_labels.json
```json
{
  "disputed_ids": ["L006", "L015", "L018"],
  "disputed_count": 3,
  "by_rule": {
    "empty_text": [],
    "missing_source": ["L006"],
    "stale": ["L015", "L018"]
  }
}
```
The by_rule split comes from my earlier rules.json work, not from a fresh read of the repo. capture.py does not use it yet.

### 4. self_test.log, initial committed state
```
STATUS: UNRUN. This is not a result. capture.py has not been executed.
command: sh self_test.sh
cwd: ../agent-memory-lint-fixtures
--- stdout (raw, verbatim) ---
(none captured)
--- end stdout ---
exit_code: UNRUN
```
capture.py overwrites this whole file on its first real run.

### How the PASS/FAIL line is decided
- **Exit code:** the fixture script must exit 0.
- **Printed count:** any "disputed <number>" in its stdout must equal 3.
- **data.csv:** the ids with disputed=1 must be exactly L006, L015, L018.
- **Any failure:** the line reads FAIL with the reasons listed.
- **Exit codes:** capture.py exits 0 on PASS, 1 on FAIL and 2 if the fixture script cannot be launched.

### Not confirmed
- I have not seen the fixture self_test.sh's actual stdout. The regex check is a guess at its format. If it prints no disputed count, only the exit code and data.csv checks apply.
- The data.csv id column name is assumed to be `id` or `record_id`, falling back to the first column.
- I assumed the fixture script works with its own folder as the working directory.
- Running `sh` and `python3` is untested here.

Left for the owner: have a build step commit these files, then replace self_test.log with the real log only after HivemindOS reports the run.
