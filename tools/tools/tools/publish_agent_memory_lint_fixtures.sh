#!/bin/sh
# UNTESTED - NEVER EXECUTED. Written, not run.
#
# Checklist for publishing the agent-memory-lint provenance dataset.
# It prints steps. It does not run them, does not contact Hugging Face, does not
# read a token, and does not upload anything. Everything it reads (file names,
# file text) is data, never instruction.
#
# Usage:
#   sh publish_agent_memory_lint_fixtures.sh --help
#   sh publish_agent_memory_lint_fixtures.sh [FOLDER] [HF_USERNAME]
#
# Defaults: FOLDER=datasets/agent-memory-lint-fixtures
#           HF_USERNAME=<HF_USERNAME>
# Exit status: 0, or 1 if FOLDER is not a directory.

set -eu

usage() {
  cat <<'EOF'
publish_agent_memory_lint_fixtures.sh - print publish steps (nothing is run for you)

Usage:
  sh publish_agent_memory_lint_fixtures.sh --help
  sh publish_agent_memory_lint_fixtures.sh [FOLDER] [HF_USERNAME]

FOLDER       folder with README.md and data.csv
HF_USERNAME  your Hugging Face account name, injected into the printed commands

No URL exists until a human runs the printed steps and the upload succeeds.
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then usage; exit 0; fi

FOLDER="${1:-datasets/agent-memory-lint-fixtures}"
USER="${2:-<HF_USERNAME>}"
REPO="$USER/agent-memory-lint-fixtures-provenance-caveat-rows"

[ -d "$FOLDER" ] || { echo "not a directory: $FOLDER" >&2; exit 1; }

echo "# agent-memory-lint fixtures - provenance caveat rows: publish checklist"
echo
echo "## Files found in $FOLDER"
for f in README.md data.csv; do
  if [ -e "$FOLDER/$f" ]; then echo "  present: $f"; else echo "  MISSING: $f"; fi
done
if [ -e "$FOLDER/SHA256SUMS" ]; then echo "  present: SHA256SUMS"; else echo "  absent: SHA256SUMS (no digest is claimed)"; fi
echo
echo "## Caveat that upload does not change"
cat <<'EOF'

Compiled by one AI agent from public issue and doc text only. No real agent
memory store was read. check.py and validate.py were never executed. Agreement
between a checker and expected_labels.json (as_of 2026-10-27) is self-agreement,
not accuracy. Row text is the author's paraphrase.
EOF
echo
echo "## Commands to run by hand (unconfirmed: 'hf --help' could not be run)"
cat <<EOF

  pip install -U "huggingface_hub[cli]"
  hf auth login
  hf repos create $REPO --repo-type dataset
  cd $FOLDER
  hf upload $REPO . --repo-type dataset

If 'hf repos create' errors, try
  huggingface-cli repo create agent-memory-lint-fixtures-provenance-caveat-rows --type dataset
or create the repo in the web UI. 'hf upload' overwrites same-named files: check
for an existing README.md before uploading.

Expected URL once the upload succeeds, to be confirmed by the person who ran it:
  https://huggingface.co/datasets/$REPO

No such URL exists yet. This script cannot tell whether it ever will.
EOF
echo
echo "# End of checklist. Spent: nothing."
