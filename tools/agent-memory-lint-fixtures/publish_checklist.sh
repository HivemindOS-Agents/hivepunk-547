#!/bin/sh
# UNTESTED - NEVER EXECUTED. Written, not run.
#
# Prints (does not run) the steps a human with a Hugging Face account would take
# to publish the agent-memory-lint-fixtures folder.
#
# This script never contacts Hugging Face, never reads a token, never uploads
# anything and never runs a command for you. It only echoes text and lists which
# expected files are present in the current directory. Treat it as a checklist.
#
# Usage:
#   sh publish_checklist.sh --help
#   sh publish_checklist.sh                 # run from datasets/agent-memory-lint-fixtures
#
# Nothing here is a verification that the dataset is correct, that check.py
# works, or that any URL exists.

set -eu

usage() {
  cat <<'EOF'
publish_checklist.sh - print the publish steps for agent-memory-lint-fixtures

Usage:
  sh publish_checklist.sh --help
  sh publish_checklist.sh [FOLDER]

Arguments:
  FOLDER   folder holding the dataset files (default: .)

Output:
  - a file-presence listing for README.md, data/records.jsonl,
    data/expected_labels.json, check.py, validate.py
  - the commands to run by hand, in order
  - the one-line self-agreement check for after check.py has been run

Exit status:
  0 always, unless FOLDER is not a directory.

Notes:
  This script does not run the printed commands. It does not upload. It holds no
  token. It is untested: nobody has executed it.
EOF
}

OUT="."
for arg in "$@"; do
  case "$arg" in
    -h|--help) usage; exit 0 ;;
    *) OUT="$arg" ;;
  esac
done

[ -d "$OUT" ] || { echo "not a directory: $OUT" >&2; exit 1; }

echo "# agent-memory-lint-fixtures - publish checklist (nothing here is run for you)"
echo
echo "## Files found in $OUT"
for f in README.md data/records.jsonl data/expected_labels.json check.py validate.py; do
  if [ -e "$OUT/$f" ]; then
    echo "  present: $f"
  else
    echo "  MISSING: $f"
  fi
done
echo
echo "## Commands to run by hand (unconfirmed: I could not run 'hf --help')"
cat <<'EOF'

  pip install -U "huggingface_hub[cli]"
  hf auth login
  hf repos create <HF_USERNAME>/agent-memory-lint-fixtures --repo-type dataset
  cd datasets/agent-memory-lint-fixtures
  sha256sum README.md data/records.jsonl data/expected_labels.json check.py validate.py > SHA256SUMS
  hf upload <HF_USERNAME>/agent-memory-lint-fixtures . --repo-type dataset

If 'hf repos create' errors, use the older form
  huggingface-cli repo create agent-memory-lint-fixtures --type dataset
or create the repository in the web UI. The upload command is unchanged.
'hf upload' overwrites same-named files: check for an existing README.md first.

No URL exists for this dataset until a human runs the steps above and the upload
succeeds. This script cannot know whether it did.
EOF
echo
echo "## One-line self-agreement check, after running check.py once"
cat <<'EOF'

  python3 check.py data/records.jsonl > /tmp/got.json && python3 -c "import json;a=json.load(open('data/expected_labels.json'))['labels'];b=json.load(open('/tmp/got.json'))['labels'];print('self-agreement' if a==b else 'MISMATCH')"

'self-agreement' means the labels and the checker agree with each other. One
author wrote the records, the labels and the checker, so that is self-agreement,
not accuracy. 'MISMATCH' is a likely outcome while check.py is untested.
No real agent memory store was involved at any point.
EOF
echo
echo "# End of checklist. Spent: nothing."
