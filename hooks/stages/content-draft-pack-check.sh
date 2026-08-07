#!/bin/sh
# Content gate - Evening quant draft-pack structural check.
#
# Advisory by default; set QF_STAGE_ENFORCE=1 to block.

set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DIR/common.sh"

qf_stage_header content-draft-pack "Evening content draft-pack check"
cd "$QF_ROOT"

warn_missing() {
  path=$1
  if [ ! -e "$path" ]; then
    qf_warn "Missing required evening content file: $path"
  fi
}

warn_grep() {
  pattern=$1
  path=$2
  label=$3
  if [ ! -f "$path" ] || ! grep -qF "$pattern" "$path"; then
    qf_warn "$path missing $label"
  fi
}

pack_root="evening_quant_content_twitter"
config="$pack_root/configs/evening_quant_content.yml"
sample="$pack_root/examples/evening_quant_content/sample_draft_pack.yml"
context="$pack_root/examples/evening_quant_content/context_sample.md"
template="$pack_root/templates/docs/evening_quant_draft_pack.md"
runtime="$pack_root/runtime/evening_quant_pipeline.py"
scheduler="$pack_root/scheduler/cron.md"

warn_missing "$config"
warn_missing "$sample"
warn_missing "$context"
warn_missing "$template"
warn_missing "$runtime"
warn_missing "$scheduler"
warn_missing "$pack_root/scheduler/evening_quant_content.cron.example"
warn_missing "$pack_root/memory/evening_quant_content/index.yaml"
warn_missing "$pack_root/specs/0005-evening-quant-content-runnable-pipeline/spec.md"

for section in "schedule:" "platform:" "content:" "sources:" "review:" "memory:" "delivery:"; do
  warn_grep "$section" "$config" "config section $section"
done

warn_grep "require_manual_approval: true" "$config" "manual approval requirement"
warn_grep "auto_post_enabled: false" "$config" "disabled autopost flag"
warn_grep "max_post_chars:" "$config" "post character limit"
warn_grep "ranked_ideas:" "$sample" "ranked ideas"
warn_grep "finished_posts:" "$sample" "finished posts"
warn_grep "thread_drafts:" "$sample" "thread drafts"
warn_grep "meme_concepts:" "$sample" "meme concepts"
warn_grep "visual_specs:" "$sample" "visual specs"
warn_grep "source_notes:" "$sample" "source notes"
warn_grep "review_findings:" "$sample" "review findings"
warn_grep "manual_approval_required: true" "$sample" "manual approval flag"
warn_grep "runtime_entrypoint:" "$config" "runtime entrypoint"
warn_grep "scheduler_profile:" "$config" "scheduler profile"
warn_grep "python evening_quant_content_twitter/runtime/evening_quant_pipeline.py" "$scheduler" "runtime command"

for agent in content_orchestrator market_context_researcher quant_angle_generator x_post_packager visual_spec_agent meme_culture_agent claim_review_agent content_memory_agent; do
  for file in README.md prompt.md instructions.md tasks.md; do
    warn_missing "$pack_root/agents/content/$agent/$file"
  done
done

tmp_dir="${TMPDIR:-/tmp}/quantsmith-evening-content-check"
rm -rf "$tmp_dir"
if command -v python >/dev/null 2>&1; then
  if ! python "$runtime" \
    --config "$config" \
    --context "$context" \
    --output-dir "$tmp_dir" \
    --generated-at "2026-08-07T22:30:00-04:00" >/dev/null 2>&1; then
    qf_warn "runtime smoke test failed: $runtime"
  else
    [ -f "$tmp_dir/draft_pack.yml" ] || qf_warn "runtime did not create draft_pack.yml"
    [ -f "$tmp_dir/draft_pack.md" ] || qf_warn "runtime did not create draft_pack.md"
    warn_grep "manual_approval_required: true" "$tmp_dir/draft_pack.yml" "runtime manual approval output"
    warn_grep "auto_post_enabled: false" "$tmp_dir/draft_pack.yml" "runtime autopost disabled output"
  fi
else
  qf_warn "python not available; runtime smoke test skipped"
fi

qf_stage_result content-draft-pack
