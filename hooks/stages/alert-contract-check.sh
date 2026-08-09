#!/bin/sh
# Alerting gate - Alert policy/contract check.
#
# When an alert policy artifact exists, verifies it declares the shared alert
# contract: event/rule id, owner, severity, deduplication, runbook, redaction,
# and a test route. See templates/data/alert_policy.md and instructions/alerting.md.
# Advisory by default; QF_STAGE_ENFORCE=1 blocks.

set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DIR/common.sh"

qf_stage_header alert-contract "Alert contract check"
cd "$QF_ROOT"

artifacts=""
for pattern in "*alert_policy*.md" "*.alerts.md" "alerts/*.md"; do
  for f in $pattern; do
    case "$f" in templates/*|prompts/*) continue ;; esac
    [ -f "$f" ] && artifacts="$artifacts $f"
  done
done

if [ -z "$artifacts" ]; then
  qf_info "No alert policy artifact detected (see templates/data/alert_policy.md)."
  qf_stage_result alert-contract
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
  check_field "$a" "rule/event id"  "rule[_ ]?id|event[_ ]?id"
  check_field "$a" "owner"          "owner|owned by|steward"
  check_field "$a" "severity"       "severity|critical|warning|info"
  check_field "$a" "deduplication"  "dedup|deduplicat|correlation"
  check_field "$a" "runbook"        "runbook|escalation|on-?call"
  check_field "$a" "redaction"      "redact|no (secrets|credentials|pii|mnpi)"
  check_field "$a" "test route"     "test route|synthetic|dry[- ]?run"
done

qf_stage_result alert-contract
