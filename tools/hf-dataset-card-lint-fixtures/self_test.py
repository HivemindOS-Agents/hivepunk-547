#!/usr/bin/env python3
"""Self-test for the dataset card linter.

Builds a clean fixture and a bad fixture in a temporary directory,
runs lint.py on each, and exits 0 only when the clean one passes and
the bad one fails."""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LINT_PY = os.path.join(HERE, "lint.py")

def _make_clean(tmp):
    """Create a clean fixture: valid README and CSV."""
    dirpath = os.path.join(tmp, "clean")
    os.mkdir(dirpath)
    # README.md with closing section
    readme = os.path.join(dirpath, "README.md")
    with open(readme, "w", encoding="utf-8") as f:
        f.write("---\ntags: test\n---\n# Clean fixture\n## What could not be checked\nNothing.\n")
    # CSV with correct cell counts
    csvpath = os.path.join(dirpath, "data.csv")
    with open(csvpath, "w", encoding="utf-8") as f:
        f.write("a,b,c\n1,2,3\n4,5,6\n")
    return dirpath

def _make_bad(tmp):
    """Create a bad fixture: missing closing section and a CSV row with wrong cell count."""
    dirpath = os.path.join(tmp, "bad")
    os.mkdir(dirpath)
    # README.md WITHOUT closing section
    readme = os.path.join(dirpath, "README.md")
    with open(readme, "w", encoding="utf-8") as f:
        f.write("---\ntags: test\n---\n# Bad fixture\nNothing else.\n")
    # CSV with one row having different cell count
    csvpath = os.path.join(dirpath, "data.csv")
    with open(csvpath, "w", encoding="utf-8") as f:
        f.write("a,b,c\n1,2\n3,4,5\n")  # first row has 2 cells, second has 3
    return dirpath

def main():
    if not os.path.isfile(LINT_PY):
        sys.stderr.write("FAIL: lint.py not found next to self_test.py\n")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmp:
        clean_dir = _make_clean(tmp)
        bad_dir = _make_bad(tmp)

        # Test clean fixture
        cp = subprocess.run(
            [sys.executable, LINT_PY, clean_dir],
            capture_output=True, text=True
        )
        if cp.returncode != 0:
            sys.stderr.write("FAIL: clean fixture returned exit code {}\n".format(cp.returncode))
            sys.stderr.write(cp.stderr)
            sys.exit(1)
        if cp.stdout.strip():
            sys.stderr.write("FAIL: clean fixture produced unexpected output:\n")
            sys.stderr.write(cp.stdout)
            sys.exit(1)
        print("clean fixture: ok")

        # Test bad fixture — must return non-zero (1)
        cp = subprocess.run(
            [sys.executable, LINT_PY, bad_dir],
            capture_output=True, text=True
        )
        if cp.returncode != 1:
            sys.stderr.write("FAIL: bad fixture returned exit code {} (expected 1)\n".format(cp.returncode))
            sys.stderr.write(cp.stderr)
            sys.exit(1)
        if not cp.stdout.strip():
            sys.stderr.write("FAIL: bad fixture produced no output\n")
            sys.exit(1)
        # Verify at least two issues: missing section and row cell mismatch
        lines = [l for l in cp.stdout.splitlines() if l.strip()]
        if not any("missing closing" in l.lower() for l in lines):
            sys.stderr.write("FAIL: bad fixture should report missing closing section\n")
            sys.exit(1)
        if not any("cells" in l.lower() for l in lines):
            sys.stderr.write("FAIL: bad fixture should report CSV cell mismatch\n")
            sys.exit(1)
        print("bad fixture: {} issues found".format(len(lines)))

    print("self-test: all checks passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
