#!/usr/bin/env python3
"""Self-test for dataset-package-manifest.

Run from this folder with no arguments and no network. Imports
dataset_package_manifest, then checks its manifest CSV and
README Files verification on synthetic package folders in a
temp directory: matching package, mismatch (missing/extra),
duplicates, missing listed file, missing folder, missing
README, missing Files section, plus CLI exit codes. Exits 0
only if all checks pass.
"""

import contextlib
import hashlib
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
        return __import__("dataset_package_manifest")
    except Exception as e:
        raise Fail("could not import dataset_package_manifest: %s: %s" % (type(e).__name__, e))


def write(folder, name, data):
    path = os.path.join(folder, name)
    if isinstance(data, str):
        data = data.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    return path


def make_pkg(folder, listed, disk):
    os.mkdir(folder)
    for name, data in disk.items():
        write(folder, name, data)
    bullets = "\n".join("- %s" % n for n in listed)
    write(folder, "README.md", "# pkg\n\n## Files\n\n%s\n" % bullets)


def main():
    try:
        mod = import_tool()
        checks = []
        with tempfile.TemporaryDirectory() as tmp:
            match = os.path.join(tmp, "match")
            payload = {"alpha.py": "x=1\n", "data.csv": "a,b\n1,2\n"}
            make_pkg(match, ["README.md", "alpha.py", "data.csv"], dict(payload, **{"README.md": "placeholder"}))
            # Rewrite README with real content so its manifest row is meaningful
            ok, problems, csv_text, rows = mod.manifest_and_verify(match)
            check(ok, "match failed: %r" % (problems,))
            check(csv_text.startswith("file_name,bytes,lines,sha256\n"), "csv header %r" % (csv_text[:60],))
            names = [r[0] for r in rows]
            check(names == sorted(names) == ["README.md", "alpha.py", "data.csv"], "sorted names %r" % (names,))
            alpha = next(r for r in rows if r[0] == "alpha.py")
            check(alpha[1] == 4 and alpha[2] == 1, "alpha row %r" % (alpha,))
            check(alpha[3] == hashlib.sha256(b"x=1\n").hexdigest(), "alpha sha256 %r" % (alpha,))
            checks.append("match case passes; CSV header, sorted rows, bytes/lines and sha256 correct")

            mismatch = os.path.join(tmp, "mismatch")
            make_pkg(mismatch, ["README.md", "alpha.py", "stray.py"], {"README.md": "x", "alpha.py": "x=1\n", "gamma.py": "g\n"})
            ok, problems, csv_text, _ = mod.manifest_and_verify(mismatch)
            joined = " ".join(problems)
            check(not ok and csv_text == "", "mismatch should fail with no CSV")
            check("missing from Files list" in joined and "gamma.py" in joined, "mismatch %r" % (problems,))
            check("missing on disk" in joined and "stray.py" in joined, "mismatch extra %r" % (problems,))
            checks.append("mismatch case reports missing (gamma.py) and extra (stray.py) with no CSV")

            dupes = os.path.join(tmp, "dupes")
            make_pkg(dupes, ["README.md", "alpha.py", "alpha.py"], {"README.md": "x", "alpha.py": "x=1\n"})
            ok, problems, _, _ = mod.manifest_and_verify(dupes)
            check(not ok and "duplicate" in " ".join(problems), "dupes %r" % (problems,))
            checks.append("duplicate case fails and names alpha.py")

            missing_file = os.path.join(tmp, "missing_file")
            make_pkg(missing_file, ["README.md", "ghost.py"], {"README.md": "x"})
            ok, problems, _, _ = mod.manifest_and_verify(missing_file)
            check(not ok and "ghost.py" in " ".join(problems), "missing-file %r" % (problems,))
            ok, problems, _, _ = mod.manifest_and_verify(os.path.join(tmp, "absent"))
            check(not ok and any("folder not found" in p for p in problems), "absent %r" % (problems,))
            no_readme = os.path.join(tmp, "no_readme"); os.mkdir(no_readme); write(no_readme, "alpha.py", "x=1\n")
            ok, problems, _, _ = mod.manifest_and_verify(no_readme)
            check(not ok and any("README.md not found" in p for p in problems), "no-readme %r" % (problems,))
            checks.append("missing-file, missing folder and missing README fail with clear messages")

            no_section = os.path.join(tmp, "no_section"); os.mkdir(no_section); write(no_section, "README.md", "# pkg\n")
            ok, problems, _, _ = mod.manifest_and_verify(no_section)
            check(not ok and any("## Files" in p for p in problems), "no-section %r" % (problems,))
            checks.append("missing Files section fails and mentions '## Files'")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["dataset_package_manifest.py", match])
            check(code == 0 and buf.getvalue().startswith("file_name,"), "CLI match %r %r" % (code, buf.getvalue()[:60]))
            buf, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
                code = mod.main(["dataset_package_manifest.py", mismatch])
            check(code == 1 and "FAIL:" in err.getvalue() and buf.getvalue() == "", "CLI mismatch %r %r" % (code, err.getvalue()))
            checks.append("CLI exits 0 with CSV for match and 1 with FAIL on stderr for mismatch")
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
