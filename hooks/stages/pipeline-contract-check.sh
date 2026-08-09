#!/bin/sh
# Data-engineering gate - Pipeline contract check.
#
# When a pipeline manifest artifact exists, verifies it declares the metadata a
# reviewable data pipeline needs: owner, schedule, inputs/outputs, retry or
# backfill, idempotency, and a runbook. See templates/data/pipeline_manifest.md
# and instructions/pipeline_engineering.md. Advisory by default; QF_STAGE_ENFORCE=1
# blocks.

set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DIR/common.sh"

qf_stage_header pipeline-contract "Pipeline contract check"
cd "$QF_ROOT"

# Find pipeline manifest artifacts by convention (exclude templates/prompts to
# avoid validating the scaffolding itself).
manifests=""
for pattern in \
  "*pipeline_manifest*.md" "*.pipeline.md" "*_pipeline.md" \
  "pipelines/*.md" "specs/*/pipeline_manifest*.md"; do
  for f in $pattern; do
    case "$f" in
      templates/*|prompts/*) continue ;;
    esac
    [ -f "$f" ] && manifests="$manifests $f"
  done
done

if [ -z "$manifests" ]; then
  qf_info "No pipeline manifest artifact detected (see templates/data/pipeline_manifest.md)."
  qf_stage_result pipeline-contract
  exit $?
fi

check_field() { # file, label, regex
  if grep -riqE "$3" "$1" 2>/dev/null; then
    qf_info "$(basename "$1"): $2 declared."
  else
    qf_warn "$(basename "$1"): $2 not declared."
  fi
}

# Deduplicate the manifest list.
seen=""
for m in $manifests; do
  case " $seen " in *" $m "*) continue ;; esac
  seen="$seen $m"

  check_field "$m" "owner"           "owner|owned by|steward"
  check_field "$m" "schedule"        "schedule|cron|cadence|frequency"
  check_field "$m" "inputs/outputs"  "input|source|output|sink"
  check_field "$m" "retry/backfill"  "retry|backfill|reprocess"
  check_field "$m" "idempotency"     "idempoten"
  check_field "$m" "runbook"         "runbook|on-?call|incident|escalation"
done

qf_stage_result pipeline-contract
