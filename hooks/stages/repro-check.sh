#!/bin/sh
# Quant gate - Reproducibility check.
#
# Checks the signals that make constitution P4 (reproducible by default) real:
# a run manifest artifact, a dependency lockfile, and seeded randomness in
# changed code. Advisory by default; set QF_STAGE_ENFORCE=1 to block.

set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DIR/common.sh"

qf_stage_header repro "Reproducibility check"
cd "$QF_ROOT"

# Run manifest / experiment record. Exclude SDK scaffolding (templates/, prompts/)
# so the templates that DEFINE a run card are not mistaken for a real one.
manifest=""
for pattern in \
  "run_card*.md" "*/run_card*.md" \
  "run_manifest*.md" "*/run_manifest*.md" \
  "experiments/*/run_card*.md" "specs/*/run_card*.md"; do
  for f in $pattern; do
    case "$f" in
      templates/*|prompts/*) continue ;;
    esac
    [ -f "$f" ] && manifest="$manifest $f"
  done
done
if [ -n "$manifest" ]; then
  qf_info "Run manifest artifact present."
else
  qf_warn "No run manifest found (see templates/docs/run_card.md) — record data snapshot, seed, config, and env."
fi

# Dependency lockfile.
if qf_glob_exists \
  "poetry.lock" "uv.lock" "Pipfile.lock" "conda-lock.yml" \
  "requirements*.txt" "environment.yml"; then
  qf_info "Dependency lockfile present."
else
  qf_warn "No dependency lockfile found — pin the environment for reproducibility."
fi

# Seeded randomness in changed Python.
changed=$(qf_changed_files)
uses_rng=0
sets_seed=0
for f in $changed; do
  case "$f" in
    *.py|*.ipynb) ;;
    *) continue ;;
  esac
  [ -f "$f" ] || continue
  if grep -nE 'np\.random|numpy\.random|random\.|torch\.|tf\.random|sample\(' "$f" >/dev/null 2>&1; then
    uses_rng=1
  fi
  if grep -nE 'seed\(|random_state\s*=|manual_seed\(' "$f" >/dev/null 2>&1; then
    sets_seed=1
  fi
done

if [ "$uses_rng" -eq 1 ] && [ "$sets_seed" -eq 0 ]; then
  qf_warn "Changed code uses randomness but sets no seed/random_state."
fi

qf_stage_result repro
