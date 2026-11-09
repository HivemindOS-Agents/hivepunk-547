~~~python
#!/usr/bin/env python3
# This self‑test runs lint.py against each fixture folder and verifies the
# expected output and exit codes. It writes a summary of the runs to
# ARTIFACTS.md.
import subprocess
import sys
import os

# Map of fixture name → expected exit code and expected output (trimmed)."""
TESTS = {
    "clean": {
        "exit": 0,
        "output": "",
    },
    "bad-rows": {
        "exit": 1,
        "output": (
            "data.csv line 2 has 2 cells (header 3)\n"
            "data.csv line 3 has 4 cells (header 3)"
        ),
    },
    "bad-card": {
        "exit": 1,
        "output": "README missing closing 'What could not be checked' section",
    },
}

ARTIFACT_PATH = os.path.join(os.path.dirname(__file__), "ARTIFACTS.md")

results = []

for name, exp in TESTS.items():
    dirpath = os.path.join(os.path.dirname(__file__), name)
    cmd = [sys.executable, "lint.py", dirpath]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
    out = proc.stdout.strip()
    failed = proc.returncode != exp["exit"] or out != exp["output"].strip()
    results.append(
        {
            "name": name,
            "exit": proc.returncode,
            "expected_exit": exp["exit"],
            "output": out,
            "expected_output": exp["output"].strip(),
            "failed": failed,
        }
    )

# Write artifacts
with open(ARTIFACT_PATH, "w", encoding="utf-8") as fh:
    fh.write("## Self‑Test Run Results\n\n")
    for r in results:
        fh.write(f"### {r['name']}\n")
        fh.write(f"- Expected exit: {r['expected_exit']}\n")
        fh.write(f"- Actual exit:   {r['exit']}\n")
        fh.write(f"- Expected output:\n````text\n{r['expected_output']}\n````\n")
        fh.write(f"- Actual output:   \n````text\n{r['output']}\n````\n")
        fh.write(f"- Pass: {not r['failed']}\n\n")

# Exit 0 only if all passes
if any(r["failed"] for r in results):
    sys.stderr.write("self‑test failed for one or more fixtures. See ARTIFACTS.md\n")
    sys.exit(1)
else:
    sys.stdout.write("self-test succeeded for all fixtures.\n")
    sys.exit(0)
~~~
