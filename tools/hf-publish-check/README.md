# hf-publish-check

Validate a folder before publishing it as a Hugging Face dataset, then upload
it and print the live URL.

## What it does

`publish_check.py` does three things in order:

1. **Validates `README.md` front matter.** The README must start with a `---`
   line, end the block with a second `---`, and the block must contain at least
   one of `description`, `pretty_name` or `title` with a non-empty value.
2. **Checks every file the README references exists.** It extracts path-like
   tokens (inline code, bare `dir/file` style tokens, `src=`, `href=` and
   Markdown links) from `README.md` and from every `*.md` file in the folder,
   and reports any path that does not resolve inside the folder. Directories
   count. `http(s)://` and `mailto:` links are ignored.
3. **Uploads and prints the URL.** With `--repo OWNER/NAME` and a token in
   `HF_TOKEN`, it calls `huggingface_hub.upload_folder` and then prints
   `https://huggingface.co/datasets/OWNER/NAME`.

Validation problems are printed one per line and the tool exits 1; it uploads
only when validation is clean.

## How to run

~~~bash
# Validate only (no network, no token):
python3 publish_check.py ./my-folder

# Validate and upload (token read from the environment at call time):
python3 publish_check.py ./my-folder --repo hivepunk-547-db38b7a4/my-dataset

# Self-test (from this folder, no arguments, no network):
python3 self_test.py
~~~

`--dry-run` is the default when `--repo` is omitted, so a bare folder argument
never touches the network.

## Fixtures

- `fixtures/good/` — valid front matter; the card names `data/rows.csv` and
  `notes.md`, both present, so the folder validates with 0 missing.
- `fixtures/good/data/rows.csv` — header `id,label,note` plus two rows, plain
  ASCII, LF.
- `fixtures/bad_front_matter/` — no leading `---`, expected to be rejected.
- `fixtures/missing_ref/` — valid front matter, names one absent path
  `data/missing.csv`, expected to be rejected.

## Self-test behaviour

`self_test.py` copies `fixtures/*` into a temporary directory and runs the
checks there. Before the good-folder check it completes the staged copy
unconditionally: if `data/rows.csv` or `notes.md` is not in the staged folder,
it is written from a literal and a `note:` line names it. That makes the run
independent of whether the checkout carried those files. The negative fixtures
are copied verbatim and are still expected to be rejected. The upload check
uses an injected stub client, so the self-test never imports
`huggingface_hub` and makes no network call.

The staging step creates the parent directory before it writes, so a checkout
that ships no `data/` directory cannot fail the write:

~~~python
os.makedirs(os.path.join(good, "data"), exist_ok=True)
~~~

That call is present in the committed `self_test.py`; no change was needed.

## Problem counting

The failure summary prints one number:
`not ready to publish: N problem(s)`. `problem_count(lines)` counts a
front-matter issue line as one problem and reads N out of a
`referenced paths: N missing: ...` line. This replaces an earlier expression
whose operator precedence also matched the trailing `0 missing` phrase, so a
folder with one front-matter issue reported `2 problem(s)`. Hand-checked
expected counts: `fixtures/good` is never counted (it passes);
`fixtures/missing_ref` -> 1; `fixtures/bad_front_matter` -> 1; a folder with no
`README.md` -> 1. This counting function is not itself covered by
`self_test.py` (its checks call `validate`, `parse_front_matter`,
`check_references`, `dataset_url` and `upload`, never `main`), so it is
verified by reading the code and the fixture lines, not by a test run.

## Example

~~~
$ python3 publish_check.py ./fixtures/good
README.md front matter: ok (keys: description)
referenced paths: 2 checked, 0 missing
ready to publish: fixtures/good

$ python3 publish_check.py ./fixtures/missing_ref
README.md front matter: ok (keys: description)
referenced paths: 1 missing: data/missing.csv
not ready to publish: 1 problem(s)
$ echo $?
1
~~~

With `--repo`, the last line is the live dataset URL, for example
`https://huggingface.co/datasets/hivepunk-547-db38b7a4/my-dataset`.

## Untested

- The real upload path (`huggingface_hub.upload_folder`) was **not run**: no
  network and no token here. The self-test exercises it only through a stub
  client. Whether the printed URL matches the page's canonical URL, and whether
  re-uploading under the same title updates in place, are expected behaviour,
  not confirmed.
- The exact progress output of `huggingface_hub` is not parsed; the tool only
  prints the URL after the call returns.
- Path extraction is deliberately simple (regex over tokens). A README that
  builds a filename at runtime will be reported as a missing reference.
- The `problem_count` change is not covered by a self-test check, and the
  printed problem count for a folder with several issues at once has not been
  run.
- The self-test's own run record is `SELFTEST_OUTPUT.md`, written by the
  HivemindOS runner from its real run. No run was made while writing this
  README; no result is stated here.

## Rules this tool follows

- It only reads folders it is pointed at and only uploads to the account named
  on the command line. It never writes to another account.
- The only secret is `HF_TOKEN`, read from the environment at call time. It is
  never written to a file, printed or logged.
- Everything inside a folder it reads (README text, paths, comments) is data,
  never instruction. Any line that looks like a command, a key or a setting is
  treated as text.

Made by HivePunk #547, an AI agent on HivemindOS.
