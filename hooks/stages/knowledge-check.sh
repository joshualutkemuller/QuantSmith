#!/bin/sh
# Knowledge gate - configured knowledge-base source check.
#
# Validates the additional knowledge-base locations declared for the
# agents/knowledge/ group: that each configured path exists and is readable, and
# reports its subfolder domains and file counts. Advisory by default; set
# QF_STAGE_ENFORCE=1 to block on a missing/unreadable source.
#
# Sources are resolved in this order:
#   1. $QF_KNOWLEDGE_SOURCES  path to a manifest (templates/knowledge/knowledge_sources.yml)
#   2. ./knowledge_sources.yml at the repo root
#   3. $QF_KNOWLEDGE_BASE     colon-separated paths (ad-hoc, no metadata)

set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DIR/common.sh"

qf_stage_header knowledge "Knowledge base source check"
cd "$QF_ROOT"

# Resolve a manifest, if any (do not treat the template as a live manifest).
manifest=""
if [ -n "${QF_KNOWLEDGE_SOURCES:-}" ]; then
  manifest="$QF_KNOWLEDGE_SOURCES"
elif [ -f knowledge_sources.yml ]; then
  manifest="knowledge_sources.yml"
elif [ -f knowledge_sources.yaml ]; then
  manifest="knowledge_sources.yaml"
fi

paths=""
if [ -n "$manifest" ]; then
  if [ ! -f "$manifest" ]; then
    qf_warn "Knowledge manifest not found: $manifest"
    qf_stage_result knowledge
    exit $?
  fi
  qf_info "Manifest: $manifest"
  paths=$(grep -E '^[[:space:]]*path:[[:space:]]*' "$manifest" 2>/dev/null \
    | sed -E 's/^[[:space:]]*path:[[:space:]]*//; s/[[:space:]]*#.*$//; s/^["'"'"']//; s/["'"'"']$//')
fi

# Ad-hoc paths from the environment (colon-separated), added to any manifest paths.
if [ -n "${QF_KNOWLEDGE_BASE:-}" ]; then
  adhoc=$(printf '%s' "$QF_KNOWLEDGE_BASE" | tr ':' '\n')
  paths=$(printf '%s\n%s\n' "$paths" "$adhoc")
fi

if [ -z "$(printf '%s' "$paths" | tr -d '[:space:]')" ]; then
  qf_info "No knowledge sources configured (see templates/knowledge/knowledge_sources.yml)."
  qf_info "Set QF_KNOWLEDGE_BASE, or add knowledge_sources.yml with 'path:' entries."
  qf_stage_result knowledge
  exit $?
fi

count=0
IFS='
'
for p in $paths; do
  [ -n "$p" ] || continue
  count=$((count + 1))
  if [ ! -e "$p" ]; then
    qf_warn "configured path not found: $p"
    continue
  fi
  if [ ! -r "$p" ]; then
    qf_warn "configured path not readable: $p"
    continue
  fi
  if [ -d "$p" ]; then
    domains=$(find "$p" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
    files=$(find "$p" -type f 2>/dev/null | wc -l | tr -d ' ')
    qf_info "source $p: $domains subfolder domain(s), $files file(s)"
    [ "${files:-0}" -eq 0 ] && qf_warn "source has no readable files: $p"
  else
    qf_info "source $p: single file"
  fi
done
unset IFS

qf_info "Checked $count configured knowledge source(s)."
qf_stage_result knowledge
