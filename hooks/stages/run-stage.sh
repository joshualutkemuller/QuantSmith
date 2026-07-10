#!/bin/sh
# Run one or all QF Workflow SDK stage checks.
#
# Usage:
#   hooks/stages/run-stage.sh                 # run all stages
#   hooks/stages/run-stage.sh testing         # run one stage
#   hooks/stages/run-stage.sh planning design # run several
#
# Stages: planning design implementation testing deployment maintenance
#
# Environment:
#   QF_STAGE_ENFORCE=1  make findings blocking (non-zero exit)
#   QF_RUN_TESTS=1      let the testing stage run the suite
#   QF_DIFF_BASE=<ref>  diff changed files against <ref> instead of the worktree

DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

ALL="planning design implementation testing deployment maintenance"
stages="$*"
[ -z "$stages" ] && stages="$ALL"

rc=0
for stage in $stages; do
  script="$DIR/${stage}-check.sh"
  if [ ! -f "$script" ]; then
    printf 'Unknown stage: %s\n' "$stage" >&2
    printf 'Valid stages: %s\n' "$ALL" >&2
    rc=2
    continue
  fi
  sh "$script" || rc=1
done

exit "$rc"
