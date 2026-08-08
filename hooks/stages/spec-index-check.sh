#!/bin/sh
# Docs gate - Spec index sync check.
#
# Verifies every tracked spec (a directory under specs/ containing spec.md) is
# listed in the spec index, specs/README.md. Keeps the index from drifting as specs
# are added, the way agent-catalog keeps agents/README.md in sync. Advisory by
# default; set QF_STAGE_ENFORCE=1 to block.

set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DIR/common.sh"

qf_stage_header spec-index "Spec index sync check"
cd "$QF_ROOT"

index="specs/README.md"
if [ ! -d specs ]; then
  qf_info "No specs/ directory; spec-index check skipped."
  qf_stage_result spec-index
  exit $?
fi
if [ ! -f "$index" ]; then
  qf_warn "Spec index missing: $index"
  qf_stage_result spec-index
  exit $?
fi

count=0
for spec in specs/*/; do
  [ -f "${spec}spec.md" ] || continue
  count=$((count + 1))
  id=$(basename "$spec")          # e.g. 0011-data-pipeline-orchestration
  if ! grep -qF "$id" "$index" 2>/dev/null; then
    qf_warn "Spec not listed in $index: $id"
  fi
done

qf_info "Checked $count spec(s) against the index."
qf_stage_result spec-index
