#!/bin/sh
# Docs gate - Relative Markdown link check.
#
# Verifies that relative links and image paths in Markdown files point at
# something that exists. External links (http/https/mailto) and pure anchors are
# skipped. Advisory by default; set QF_STAGE_ENFORCE=1 to block.

set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DIR/common.sh"

qf_stage_header docs-link "Relative Markdown link check"
cd "$QF_ROOT"

md_files=$(find . -type f -name '*.md' -not -path './.git/*' | sort)
checked=0

for f in $md_files; do
  base=$(dirname "$f")
  # Extract link/image targets: the "](target" portion, up to space or ')'.
  targets=$(grep -oE '\]\([^)[:space:]]+' "$f" 2>/dev/null | sed 's/^](//' || true)
  for t in $targets; do
    # Strip a trailing anchor (#section).
    path=${t%%#*}
    [ -n "$path" ] || continue
    case "$path" in
      http://*|https://*|mailto:*|tel:*|ftp://*|//*) continue ;;
    esac
    if [ "${path#/}" != "$path" ]; then
      resolved="$QF_ROOT/${path#/}"        # repo-root-relative
    else
      resolved="$base/$path"               # file-relative
    fi
    checked=$((checked + 1))
    if [ ! -e "$resolved" ]; then
      qf_warn "$f: broken link -> $t"
    fi
  done
done

qf_info "Checked $checked relative link(s) across Markdown files."
qf_stage_result docs-link
