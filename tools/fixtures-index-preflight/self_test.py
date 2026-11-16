#!/usr/bin/env python3
"""Self-test for fixtures-index-preflight.

Run from this folder with no arguments and no network. It imports the tool's
own code (preflight), builds synthetic source folders in a temp directory,
and checks:

  1. the upload set is exactly the three expected paths;
  2. SELFTEST_OUTPUT.md, .git and __pycache__ are excluded, each with a reason;
  3. the recorded sha256 equals a fresh hash of the file;
  4. a listing that matches verifies with ok True;
  5. a listing with one missing and one extra path fails and names both;
  6. a folder without README.md yields STOP and exit 1 from the CLI;
  7. a folder that does not exist yields STOP and exit 1 from the CLI;
  8. the listing parser ignores '#' and blank lines;
  9. CLI exit codes are 0 for list, 0 for verify on a match, 1 for verify on
     a mismatch, 1 for check without README.md, 1 for check on a missing dir.

Exits 0 only when every check passes.
"""

import hashlib
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
        return __import__("preflight")
    except Exception as e:
        raise Fail("could not import preflight: %s: %s" % (type(e).__name__, e))


def make_tree(base):
    """Create a synthetic folder with README.md, two data files and clutter."""
    src = os.path.join(base, "fixtures-index-v4")
    os.makedirs(os.path.join(src, "data"), exist_ok=True)
    with open(os.path.join(src, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("# synthetic card\n")
    with open(os.path.join(src, "data", "a.csv"), "w", encoding="utf-8") as fh:
        fh.write("col\n1\n")
    with open(os.path.join(src, "data", "b.md"), "w", encoding="utf-8") as fh:
        fh.write("text\n")
    with open(os.path.join(src, "SELFTEST_OUTPUT.md"), "w", encoding="utf-8") as fh:
        fh.write("self-test: all checks passed\n")
    os.makedirs(os.path.join(src, ".git"), exist_ok=True)
    with open(os.path.join(src, ".git", "HEAD"), "w", encoding="utf-8") as fh:
        fh.write("ref: refs/heads/main\n")
    os.makedirs(os.path.join(src, "__pycache__"), exist_ok=True)
    with open(os.path.join(src, "__pycache__", "x.pyc"), "w", encoding="utf-8") as fh:
        fh.write("bytes\n")
    return src


def test_upload_set(mod, src):
    manifest, stop = mod.build_manifest(src)
    check(stop is None, "build_manifest stopped on a good folder: %s" % stop)
    paths = [f["path"] for f in manifest["files"]]
    want = ["README.md", "data/a.csv", "data/b.md"]
    check(paths == want, "upload set is %r, expected %r" % (paths, want))
    return "upload set is exactly %r" % (paths,)


def test_exclusions(mod, src):
    manifest, _ = mod.build_manifest(src)
    reasons = {e["path"]: e["reason"] for e in manifest["excluded"]}
    for name in ("SELFTEST_OUTPUT.md", ".git", "__pycache__"):
        check(name in reasons, "%s not excluded" % name)
        check(bool(reasons[name].strip()), "%s excluded without a reason" % name)
    return "excluded with reasons: SELFTEST_OUTPUT.md, .git, __pycache__"


def test_hashes(mod, src):
    manifest, _ = mod.build_manifest(src)
    for entry in manifest["files"]:
        full = os.path.join(src, entry["path"].replace("/", os.sep))
        with open(full, "rb") as fh:
            fresh = hashlib.sha256(fh.read()).hexdigest()
        check(fresh == entry["sha256"],
              "sha256 mismatch for %s" % entry["path"])
        check(os.path.getsize(full) == entry["bytes"],
              "byte count mismatch for %s" % entry["path"])
    return "sha256 and byte counts match a fresh hash for every file"


def test_verify_match(mod, src, base):
    manifest, _ = mod.build_manifest(src)
    listing = os.path.join(base, "listing_ok.txt")
    with open(listing, "w", encoding="utf-8") as fh:
        fh.write("# copied from the dataset page\n\nREADME.md\ndata/a.csv\ndata/b.md\n")
    ok, problems, summary = mod.verify(manifest, listing)
    check(ok, "matching listing failed: %r (%s)" % (problems, summary))
    return "matching listing verifies ok (%s)" % summary


def test_verify_mismatch(mod, src, base):
    manifest, _ = mod.build_manifest(src)
    listing = os.path.join(base, "listing_bad.txt")
    with open(listing, "w", encoding="utf-8") as fh:
        fh.write("README.md\ndata/b.md\ndata/extra.csv\n")
    ok, problems, _ = mod.verify(manifest, listing)
    check(not ok, "mismatched listing verified ok")
    blob = " | ".join(problems)
    check("data/a.csv" in blob, "missing path not named: %s" % blob)
    check("data/extra.csv" in blob, "extra path not named: %s" % blob)
    return "mismatch names both data/a.csv (missing) and data/extra.csv (extra)"


def test_parser(mod):
    paths = mod.parse_listing("# comment\n\n./README.md\n  data/a.csv  \n")
    check(paths == ["README.md", "data/a.csv"],
          "parser produced %r" % (paths,))
    return "parser ignores comments and blanks, strips ./ and spaces"


def test_stop_no_readme(mod, base):
    src = os.path.join(base, "no_readme")
    os.makedirs(src, exist_ok=True)
    manifest, stop = mod.build_manifest(src)
    check(manifest is None and stop and stop.startswith("STOP:"),
          "no-README folder did not stop: %r / %r" % (manifest, stop))
    code = mod.main(["preflight.py", "check", src])
    check(code == 1, "check on no-README folder returned %r, expected 1" % code)
    return "no README.md: STOP and exit 1"


def test_stop_missing_dir(mod, base):
    src = os.path.join(base, "not_there")
    manifest, stop = mod.build_manifest(src)
    check(manifest is None and stop and stop.startswith("STOP:"),
          "missing folder did not stop: %r / %r" % (manifest, stop))
    code = mod.main(["preflight.py", "check", src])
    check(code == 1, "check on missing folder returned %r, expected 1" % code)
    return "missing folder: STOP and exit 1"


def test_cli_codes(mod, src, base):
    json_out = os.path.join(base, "manifest.json")
    code = mod.main(["preflight.py", "list", src, "--json", json_out])
    check(code == 0, "list returned %r, expected 0" % code)
    check(os.path.isfile(json_out), "list did not write the manifest")
    listing = os.path.join(base, "listing_ok.txt")
    code = mod.main(["preflight.py", "verify", json_out, listing])
    check(code == 0, "verify on a match returned %r, expected 0" % code)
    bad = os.path.join(base, "listing_bad.txt")
    code = mod.main(["preflight.py", "verify", json_out, bad])
    check(code == 1, "verify on a mismatch returned %r, expected 1" % code)
    return "CLI codes: list 0, verify match 0, verify mismatch 1"


def main():
    try:
        mod = import_tool()
        with tempfile.TemporaryDirectory() as base:
            src = make_tree(base)
            lines = [
                test_upload_set(mod, src),
                test_exclusions(mod, src),
                test_hashes(mod, src),
                test_verify_match(mod, src, base),
                test_verify_mismatch(mod, src, base),
                test_parser(mod),
                test_stop_no_readme(mod, base),
                test_stop_missing_dir(mod, base),
                test_cli_codes(mod, src, base),
            ]
    except Fail as e:
        sys.stderr.write("FAIL: %s\n" % e)
        return 1
    except Exception as e:
        sys.stderr.write("FAIL: unexpected %s: %s\n" % (type(e).__name__, e))
        return 1
    for line in lines:
        print(line)
    print("self-test: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
