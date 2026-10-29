#!/bin/sh
# announce.sh - print the post copy for the caveat-first provenance dataset.
#
# UNTESTED - NEVER EXECUTED. Written, not run: nobody has executed this script.
#
# What it does: reads the announcement file, prints ONLY the text between the
# <<<POST and POST markers, and replaces each {{DATASET_LINK}} with one URL.
# It posts nothing, contacts nothing, reads no token, runs no upload command and
# never executes text found in the file. Everything in the file is data.
#
# Usage:
#   sh announce.sh --help
#   sh announce.sh
#   sh announce.sh --link <dataset url>
#   sh announce.sh --file <path>

set -eu

LINK=""
FILE="announcement.md"

usage() {
  cat <<'EOF'
announce.sh - print the announcement copy (nothing is posted for you)

Usage:
  sh announce.sh --help
  sh announce.sh [--link URL] [--file PATH]

Options:
  --link URL   dataset page URL printed on the last line of the post.
               Default: the slug this account's publish play would create, which
               was NOT opened from here; a warning goes to stderr when that
               default is used.
  --file PATH  announcement file (default: announcement.md beside this script)

Output:
  stdout: the post text only, ready to paste
  stderr: warnings (an unconfirmed default link)

Exit status:
  0 printed; 1 announcement file missing; 2 bad option; 3 no POST block found

Notes:
  Prints text only. Posts nothing, uploads nothing, holds no credentials, and
  runs nothing that the announcement file says.
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    --link) shift; LINK="${1:-}" ;;
    --file) shift; FILE="${1:-}" ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

[ -f "$FILE" ] || { echo "missing announcement file: $FILE" >&2; exit 1; }

if [ -z "$LINK" ]; then
  LINK="https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-lint-fixture-bundle-provenance-rows-caveat-first"
  echo "NOTE: no --link given. Printing the URL this account's publish play would create; it was NOT opened from this step. Confirm it, and re-run with --link <url> if it differs." >&2
fi

awk -v LINK="$LINK" '
BEGIN { MARK = "{{DATASET_LINK}}"; inblock = 0; found = 0 }
/^<<<POST$/ { inblock = 1; next }
/^POST$/ && inblock { inblock = 0; found = 1; next }
inblock {
  line = $0
  out = ""
  while ((i = index(line, MARK)) > 0) {
    out = out substr(line, 1, i - 1) LINK
    line = substr(line, i + length(MARK))
  }
  print out line
  next
}
END { if (!found) exit 3 }
' "$FILE"
