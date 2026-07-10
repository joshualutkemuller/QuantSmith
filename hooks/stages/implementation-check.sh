#!/bin/sh
# Stage 3 - Coding & Implementation gate.
#
# Catches avoidable implementation issues in changed files: committed secrets,
# large binaries, leftover notebook outputs, and debug markers. Runs available
# formatters/linters when present and skips them cleanly when absent.
# Advisory by default.

set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DIR/common.sh"

qf_stage_header implementation "Code hygiene & reproducibility check"
cd "$QF_ROOT"

changed=$(qf_changed_files)

if [ -z "$changed" ]; then
  qf_info "No changed files detected."
  qf_stage_result implementation
  exit $?
fi

# Secret-ish patterns in changed text files.
for f in $changed; do
  [ -f "$f" ] || continue
  case "$f" in
    *.png|*.jpg|*.jpeg|*.gif|*.pdf|*.parquet|*.pkl|*.h5|*.zip) continue ;;
  esac
  if grep -Eiq '(aws_secret_access_key|-----BEGIN [A-Z ]*PRIVATE KEY-----|api[_-]?key[[:space:]]*=|secret[[:space:]]*=[[:space:]]*["'"'"'][A-Za-z0-9]{16,})' "$f" 2>/dev/null; then
    qf_warn "Possible secret in $f"
  fi
done

# Large added files (> 5 MB).
for f in $changed; do
  [ -f "$f" ] || continue
  size=$(wc -c < "$f" 2>/dev/null || echo 0)
  if [ "$size" -gt 5242880 ]; then
    qf_warn "Large file (${size} bytes): $f — consider Git LFS or an artifact store."
  fi
done

# Notebooks with saved outputs.
for f in $changed; do
  case "$f" in
    *.ipynb)
      if grep -q '"output_type"' "$f" 2>/dev/null; then
        qf_warn "Notebook with saved outputs: $f — clear outputs before commit."
      fi
      ;;
  esac
done

# Debug / leftover markers in changed source.
for f in $changed; do
  case "$f" in
    *.py)
      if grep -Eq '(^|[^A-Za-z])(pdb\.set_trace|breakpoint\(\))' "$f" 2>/dev/null; then
        qf_warn "Debug breakpoint left in $f"
      fi
      ;;
  esac
done

# Optional formatter/linter, only if installed and Python changed.
py_changed=$(printf '%s\n' "$changed" | grep -E '\.py$' || true)
if [ -n "$py_changed" ]; then
  if command -v ruff >/dev/null 2>&1; then
    # shellcheck disable=SC2086
    if ! ruff check $py_changed >/dev/null 2>&1; then
      qf_warn "ruff reported lint issues in changed Python files."
    else
      qf_info "ruff clean."
    fi
  else
    qf_info "ruff not installed; skipping Python lint."
  fi
fi

qf_stage_result implementation
