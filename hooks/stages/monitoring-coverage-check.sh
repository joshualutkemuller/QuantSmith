#!/bin/sh
# Monitoring gate - Monitoring coverage check.
#
# When a monitoring plan artifact exists, verifies each production risk declares a
# metric, a threshold/baseline, an owner, an alert, a runbook, and a review cadence.
# See templates/docs/model_monitoring_plan.md and instructions/monitoring.md.
# Advisory by default; QF_STAGE_ENFORCE=1 blocks.

set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DIR/common.sh"

qf_stage_header monitoring-coverage "Monitoring coverage check"
cd "$QF_ROOT"

artifacts=""
for pattern in "*monitoring_plan*.md" "*_monitoring.md" "monitoring/*.md"; do
  for f in $pattern; do
    case "$f" in templates/*|prompts/*) continue ;; esac
    [ -f "$f" ] && artifacts="$artifacts $f"
  done
done

if [ -z "$artifacts" ]; then
  qf_info "No monitoring plan artifact detected (see templates/docs/model_monitoring_plan.md)."
  qf_stage_result monitoring-coverage
  exit $?
fi

check_field() {
  if grep -riqE "$3" "$1" 2>/dev/null; then qf_info "$(basename "$1"): $2 declared."
  else qf_warn "$(basename "$1"): $2 not declared."; fi
}

seen=""
for a in $artifacts; do
  case " $seen " in *" $a "*) continue ;; esac
  seen="$seen $a"
  check_field "$a" "metric"            "metric|indicator|kpi"
  check_field "$a" "threshold/baseline" "threshold|baseline|budget|slo"
  check_field "$a" "owner"             "owner|owned by|steward"
  check_field "$a" "alert"             "alert|page|notify"
  check_field "$a" "runbook"           "runbook|escalation|on-?call"
  check_field "$a" "review cadence"    "cadence|review|daily|weekly|monthly"
done

qf_stage_result monitoring-coverage
