#!/bin/sh
# Stage 1 - Planning & Requirements Analysis gate.
#
# Encourages that non-trivial work carries a requirements artifact with scope
# and acceptance criteria before it moves downstream. Advisory by default.

set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DIR/common.sh"

qf_stage_header planning "Requirements & scope check"
cd "$QF_ROOT"

# Look for any requirements / planning artifact in common locations.
if qf_glob_exists \
  "requirements*.md" "REQUIREMENTS*.md" \
  "docs/requirements*.md" "docs/planning*.md" \
  "research_plan*.md" "docs/research_plan*.md"; then
  found_req=1
else
  found_req=0
fi

if [ "$found_req" -eq 0 ]; then
  qf_warn "No requirements/planning doc found (see templates and prompts/research_plan.md)."
else
  qf_info "Requirements/planning artifact present."
  # If a requirements doc exists, nudge for acceptance criteria.
  if ! grep -riq "acceptance criteria" . --include="*.md" 2>/dev/null; then
    qf_warn "No 'Acceptance Criteria' found in Markdown docs."
  else
    qf_info "Acceptance criteria referenced."
  fi
fi

qf_stage_result planning
