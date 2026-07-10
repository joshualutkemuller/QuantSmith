#!/bin/sh
# Stage 2 - Design & Architecture gate.
#
# Nudges that changes touching substantial code or pipelines have a design
# artifact capturing interfaces, data flow, and trade-offs. Advisory by default.

set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DIR/common.sh"

qf_stage_header design "Design artifact & trade-off check"
cd "$QF_ROOT"

if qf_glob_exists \
  "design*.md" "DESIGN*.md" \
  "docs/design*.md" "docs/architecture*.md" \
  "adr/*.md" "docs/adr/*.md" "rfc*.md" "docs/rfc*.md"; then
  found_design=1
else
  found_design=0
fi

if [ "$found_design" -eq 0 ]; then
  qf_warn "No design/architecture doc found (see agents/design_architecture)."
else
  qf_info "Design/architecture artifact present."
  if ! grep -riq -e "trade-off" -e "tradeoff" -e "alternatives considered" . --include="*.md" 2>/dev/null; then
    qf_warn "Design docs do not record trade-offs or rejected alternatives."
  else
    qf_info "Trade-offs / alternatives documented."
  fi
fi

qf_stage_result design
