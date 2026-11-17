#!/usr/bin/env python3
"""Self-test for package-list-check.

Run from this folder with no arguments and no network. Imports
package_list_check, then checks it on synthetic package folders
in a temp directory: a matching folder, a mismatched folder
(missing/extra), a folder with duplicate list entries, and
missing-file cases (listed file absent on disk, missing folder,
missing README). Also checks CLI exit codes. Exits 0 only if
all checks pass.
"""

import contextlib
import io
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


class Fail(Exception):
    pass


def check(cond, msg):
    if not cond:
        raise Fail(msg)


def import_tool():
    sys.dont_write_bytecode = True
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    try:
        return __import__("package_list_check")
    except Exception as e:
        raise Fail("could not import package_list_check: %s: %s" % (type(e).__name__, e))


def write(folder, name, data="x\n"):
    path = os.path.join(folder, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(data)
    return path


def make_pkg(folder, listed, disk_files):
    os.mkdir(folder)
    for name in disk_files:
        write(folder, name)
    bullets = "\n".join("- %s" % n for n in listed)
    write(folder, "README.md", "# pkg\n\n## Files\n\n%s\n" % bullets)


def main():
    try:
        mod = import_tool()
        checks = []
        with tempfile.TemporaryDirectory() as tmp:
            match = os.path.join(tmp, "match")
            make_pkg(match, ["README.md", "alpha.py", "data.csv"], ["README.md", "alpha.py", "data.csv"])
            ok, problems, listed, on_disk = mod.verify(match)
            check(ok, "match fixture failed: %r listed=%r disk=%r" % (problems, listed, on_disk))
            check(sorted(listed) == ["README.md", "alpha.py", "data.csv"], "match listed %r" % (listed,))
            checks.append("match case passes with exit-0 data")

            mismatch = os.path.join(tmp, "mismatch")
            # disk has gamma.py not listed; list has stray.py not on disk
            make_pkg(mismatch, ["README.md", "alpha.py", "stray.py"], ["README.md", "alpha.py", "gamma.py"])
            ok, problems, listed, on_disk = mod.verify(mismatch)
            joined = " ".join(problems)
            check(not ok, "mismatch fixture should fail")
            check("missing from Files list" in joined and "gamma.py" in joined, "mismatch problems %r" % (problems,))
            check("missing on disk" in joined and "stray.py" in joined, "mismatch extra %r" % (problems,))
            checks.append("mismatch case reports missing (gamma.py) and extra (stray.py)")

            dupes = os.path.join(tmp, "dupes")
            make_pkg(dupes, ["README.md", "alpha.py", "alpha.py"], ["README.md", "alpha.py"])
            ok, problems, listed, on_disk = mod.verify(dupes)
            joined = " ".join(problems)
            check(not ok and "duplicate" in joined and "alpha.py" in joined, "dupes problems %r" % (problems,))
            checks.append("duplicate case fails and names alpha.py")

            missing_file = os.path.join(tmp, "missing_file")
            make_pkg(missing_file, ["README.md", "ghost.py"], ["README.md"])
            ok, problems, listed, on_disk = mod.verify(missing_file)
            joined = " ".join(problems)
            check(not ok and "ghost.py" in joined and "missing on disk" in joined, "missing-file problems %r" % (problems,))
            checks.append("missing-file case (listed but absent on disk) fails and names ghost.py")

            no_readme = os.path.join(tmp, "no_readme")
            os.mkdir(no_readme)
            write(no_readme, "alpha.py")
            ok, problems, listed, on_disk = mod.verify(no_readme)
            check(not ok and any("README.md not found" in p for p in problems), "no-readme %r" % (problems,))
            ok, problems, listed, on_disk = mod.verify(os.path.join(tmp, "absent"))
            check(not ok and any("folder not found" in p for p in problems), "absent folder %r" % (problems,))
            checks.append("missing README and missing folder fail with clear messages")

            no_section = os.path.join(tmp, "no_section")
            os.mkdir(no_section)
            write(no_section, "README.md", "# pkg\n\nNo list here.\n")
            ok, problems, listed, on_disk = mod.verify(no_section)
            check(not ok and any("## Files" in p for p in problems), "no-section %r" % (problems,))
            checks.append("missing Files section fails and mentions '## Files'")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["package_list_check.py", match])
            check(code == 0 and buf.getvalue().startswith("ok:"), "CLI match %r %r" % (code, buf.getvalue()))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["package_list_check.py", mismatch])
            check(code == 1 and "FAIL:" in buf.getvalue(), "CLI mismatch %r %r" % (code, buf.getvalue()))
            checks.append("CLI exits 0 with ok for match and 1 with FAIL for mismatch")
    except Fail as e:
        sys.stderr.write("FAIL: %s\n" % e)
        return 1
    except Exception as e:
        sys.stderr.write("FAIL: unexpected %s: %s\n" % (type(e).__name__, e))
        return 1
    for line in checks:
        print(line)
    print("self-test: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
