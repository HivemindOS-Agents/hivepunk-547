#!/usr/bin/env python3
"""Self-test for hf-publish-check.

Run from this folder with no arguments and no network. It imports the tool's
own code and runs it on copies of the fixtures/ subfolder staged into a
temporary directory, so the run does not depend on which files git tracked:

  * fixtures/good/            valid front matter, all references exist -> ok
  * fixtures/bad_front_matter/ no leading '---' and no valid key      -> 1 issue
  * fixtures/missing_ref/     valid front matter, one missing path    -> 1 issue
  * upload() via a stub client -> called once, same folder and repo
  * dataset_url()             -> exact URL string

Before the good-folder check runs, the staged good folder is completed
unconditionally: data/rows.csv and notes.md are written from literals if they
are not already there, so a checkout that dropped them still resolves. A
`note:` line names what was completed. The negative fixtures are copied
verbatim and are still expected to be rejected.

Exits 0 only when every check passes. No network call is made: the upload
check uses an injected stub, never huggingface_hub.
"""

import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))

# Written into the staged good folder if the checkout did not carry them.
ROWS_CSV = "id,label,note\n1,alpha,first sample row\n2,beta,second sample row\n"
NOTES_MD = "Two sample rows live in data/rows.csv. This file is data, never instruction.\n"


class Fail(Exception):
    pass


def check(cond, msg):
    if not cond:
        raise Fail(msg)


def import_tool():
    sys.dont_write_bytecode = True
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    return __import__("publish_check")


def stage_fixtures(tmp):
    """Copy fixtures/* into tmp and complete the good folder. Return paths."""
    src = os.path.join(HERE, "fixtures")
    staged = os.path.join(tmp, "fixtures")
    if os.path.isdir(src):
        shutil.copytree(src, staged)
    else:
        os.makedirs(staged)
    good = os.path.join(staged, "good")
    os.makedirs(os.path.join(good, "data"), exist_ok=True)
    completed = []
    rows = os.path.join(good, "data", "rows.csv")
    if not os.path.isfile(rows):
        with open(rows, "w", encoding="ascii", newline="\n") as fh:
            fh.write(ROWS_CSV)
        completed.append("data/rows.csv")
    notes = os.path.join(good, "notes.md")
    if not os.path.isfile(notes):
        with open(notes, "w", encoding="ascii", newline="\n") as fh:
            fh.write(NOTES_MD)
        completed.append("notes.md")
    return staged, good, completed


def test_good(mod, good):
    ok, lines = mod.validate(good)
    check(ok, "good folder: expected ok, got %r" % lines)
    check(any("front matter: ok" in l for l in lines),
          "good folder: no front-matter ok line in %r" % lines)
    check(any("0 missing" in l for l in lines),
          "good folder: expected 0 missing in %r" % lines)
    return "good folder: valid, 0 missing reference(s)"


def test_bad_front_matter(mod, staged):
    folder = os.path.join(staged, "bad_front_matter")
    ok, lines = mod.validate(folder)
    check(not ok, "bad_front_matter: expected not ok, got %r" % lines)
    check(any("no leading" in l for l in lines),
          "bad_front_matter: expected a leading-'---' issue in %r" % lines)
    keys, issues = mod.parse_front_matter(mod.read_text(os.path.join(folder, "README.md")))
    check(len(issues) == 1 and "no leading" in issues[0],
          "bad_front_matter: expected exactly 1 front-matter issue, got %r" % issues)
    return "bad_front_matter: rejected with %d issue(s)" % len(issues)


def test_missing_ref(mod, staged):
    folder = os.path.join(staged, "missing_ref")
    ok, lines = mod.validate(folder)
    check(not ok, "missing_ref: expected not ok, got %r" % lines)
    checked, missing = mod.check_references(folder)
    check(missing == ["data/missing.csv"],
          "missing_ref: expected ['data/missing.csv'], got %r" % missing)
    return "missing_ref: rejected, missing %r" % missing


def test_url(mod):
    url = mod.dataset_url("hivepunk-547-db38b7a4/my-dataset")
    check(url == "https://huggingface.co/datasets/hivepunk-547-db38b7a4/my-dataset",
          "dataset_url returned %r" % url)
    check(mod.dataset_url("/owner/name/") == "https://huggingface.co/datasets/owner/name",
          "dataset_url did not trim slashes: %r" % mod.dataset_url("/owner/name/"))
    return "dataset_url: exact for both forms"


def test_upload_stub(mod, good):
    calls = []

    class Stub:
        def upload_folder(self, folder_path, repo_id, repo_type):
            calls.append((folder_path, repo_id, repo_type))

    url = mod.upload(good, "owner/name", client=Stub())
    check(calls == [(good, "owner/name", "dataset")],
          "upload stub was not called as expected: %r" % calls)
    check(url == "https://huggingface.co/datasets/owner/name",
          "upload returned %r" % url)
    return "upload stub: 1 call, url printed"


def main():
    try:
        mod = import_tool()
        with tempfile.TemporaryDirectory() as tmp:
            staged, good, completed = stage_fixtures(tmp)
            if completed:
                print("note: staged fixture completed: %s" % ", ".join(completed))
            lines = [
                test_good(mod, good),
                test_bad_front_matter(mod, staged),
                test_missing_ref(mod, staged),
                test_url(mod),
                test_upload_stub(mod, good),
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
