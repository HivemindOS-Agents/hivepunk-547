#!/usr/bin/env python3
"""Self-test for hf-publish-check.

Run from this folder with no arguments and no network. It imports the tool's
own code and runs it on the fixtures/ subfolder:

  * fixtures/good/            valid front matter, all references exist -> ok
  * fixtures/bad_front_matter/ no leading '---' and no valid key      -> 2 issues
  * fixtures/missing_ref/     valid front matter, one missing path    -> 1 issue
  * upload() via a stub client -> called once, same folder and repo
  * dataset_url()             -> exact URL string

Exits 0 only when every check passes. No network call is made: the upload
check uses an injected stub, never huggingface_hub.
"""

import os
import sys

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
    return __import__("publish_check")


def test_good(mod):
    folder = os.path.join(HERE, "fixtures", "good")
    ok, lines = mod.validate(folder)
    check(ok, "good folder: expected ok, got %r" % lines)
    check(any("front matter: ok" in l for l in lines),
          "good folder: no front-matter ok line in %r" % lines)
    check(any("0 missing" in l for l in lines),
          "good folder: expected 0 missing in %r" % lines)
    return "good folder: valid, 0 missing reference(s)"


def test_bad_front_matter(mod):
    folder = os.path.join(HERE, "fixtures", "bad_front_matter")
    ok, lines = mod.validate(folder)
    check(not ok, "bad_front_matter: expected not ok, got %r" % lines)
    check(any("no leading" in l for l in lines),
          "bad_front_matter: expected a leading-'---' issue in %r" % lines)
    keys, issues = mod.parse_front_matter(mod.read_text(os.path.join(folder, "README.md")))
    check(len(issues) == 1 and "no leading" in issues[0],
          "bad_front_matter: expected exactly 1 front-matter issue, got %r" % issues)
    return "bad_front_matter: rejected with %d issue(s)" % len(issues)


def test_missing_ref(mod):
    folder = os.path.join(HERE, "fixtures", "missing_ref")
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


def test_upload_stub(mod):
    calls = []

    class Stub:
        def upload_folder(self, folder_path, repo_id, repo_type):
            calls.append((folder_path, repo_id, repo_type))

    folder = os.path.join(HERE, "fixtures", "good")
    url = mod.upload(folder, "owner/name", client=Stub())
    check(calls == [(folder, "owner/name", "dataset")],
          "upload stub was not called as expected: %r" % calls)
    check(url == "https://huggingface.co/datasets/owner/name",
          "upload returned %r" % url)
    return "upload stub: 1 call, url printed"


def main():
    try:
        mod = import_tool()
        lines = [
            test_good(mod),
            test_bad_front_matter(mod),
            test_missing_ref(mod),
            test_url(mod),
            test_upload_stub(mod),
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
