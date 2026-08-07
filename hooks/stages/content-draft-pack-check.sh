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

config="configs/evening_quant_content.yml"
sample="examples/evening_quant_content/sample_draft_pack.yml"
template="templates/docs/evening_quant_draft_pack.md"

warn_missing "$config"
warn_missing "$sample"
warn_missing "$template"
warn_missing "memory/evening_quant_content/index.yaml"

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

qf_stage_result content-draft-pack