#!/bin/sh
# Security gate - Secret leak scan.
#
# Detects credentials committed to the tree. Prefers a real scanner (gitleaks,
# then detect-secrets) when installed; otherwise falls back to a high-signal
# regex scan of changed code/config files. Advisory by default; set
# QF_STAGE_ENFORCE=1 to block (recommended in CI).
#
# Allowlisting:
#   - add a path glob per line to .secretscanignore to skip files
#   - append the marker  qf:allow-secret  to a line to ignore that line
#
# The fallback intentionally skips documentation and SDK scaffolding
# (*.md, agents/, templates/, prompts/, instructions/, docs/, examples/, hooks/)
# so instructional text about secrets is not flagged as a secret.

set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DIR/common.sh"

qf_stage_header secret-scan "Secret leak scan"
cd "$QF_ROOT"

# Prefer a dedicated scanner if present; trust its exit code.
if command -v gitleaks >/dev/null 2>&1; then
  if gitleaks detect --no-git --redact --source . >/dev/null 2>&1; then
    qf_info "gitleaks: no findings."
  else
    qf_warn "gitleaks reported potential secrets (run 'gitleaks detect --no-git -v' for detail)."
  fi
  qf_stage_result secret-scan
  exit $?
elif command -v detect-secrets >/dev/null 2>&1; then
  if detect-secrets scan >/dev/null 2>&1; then
    qf_info "detect-secrets ran (review its baseline for findings)."
  else
    qf_warn "detect-secrets reported an issue."
  fi
  qf_stage_result secret-scan
  exit $?
fi

qf_info "No dedicated scanner found; using built-in regex fallback."

# Load path-glob allowlist.
ignore_globs=""
if [ -f .secretscanignore ]; then
  ignore_globs=$(grep -vE '^\s*(#|$)' .secretscanignore 2>/dev/null || true)
fi

path_ignored() {
  case "$1" in
    *.md|*.example|.env.example) return 0 ;;
    agents/*|templates/*|prompts/*|instructions/*|docs/*|examples/*|hooks/*|.githooks/*) return 0 ;;
  esac
  for g in $ignore_globs; do
    # shellcheck disable=SC2254
    case "$1" in $g) return 0 ;; esac
  done
  return 1
}

# High-signal secret patterns (real token formats + credentialed URLs).
TOKEN_RE='AKIA[0-9A-Z]{16}|ghp_[0-9A-Za-z]{36}|github_pat_[0-9A-Za-z_]{22,}|xox[baprs]-[0-9A-Za-z-]{10,}|AIza[0-9A-Za-z_-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY-----|[A-Za-z][A-Za-z0-9+.-]*://[^:@/[:space:]]+:[^@/[:space:]]+@'
# Generic "key = long-quoted-value" assignments (filtered for placeholders below).
ASSIGN_RE='(api[_-]?key|secret|token|password|passwd|pwd|access[_-]?key)["'"'"' ]*[:=][[:space:]]*["'"'"'][^"'"'"']{12,}["'"'"']'
PLACEHOLDER_RE='example|placeholder|changeme|change-me|your[_-]|xxxx|<[^>]+>|dummy|redacted|fake|sample|\.\.\.|test[_-]?key'

changed=$(qf_changed_files)
scanned=0
for f in $changed; do
  [ -f "$f" ] || continue
  path_ignored "$f" && continue
  case "$f" in
    *.png|*.jpg|*.jpeg|*.gif|*.pdf|*.parquet|*.pkl|*.h5|*.zip|*.gz) continue ;;
  esac
  scanned=$((scanned + 1))

  # Token-format matches (skip lines with an allow marker).
  while IFS= read -r line; do
    [ -n "$line" ] || continue
    case "$line" in *qf:allow-secret*) continue ;; esac
    qf_warn "$f: possible secret — $(printf '%s' "$line" | sed 's/^[0-9]*://' | cut -c1-60)"
  done <<EOF
$(grep -nE "$TOKEN_RE" "$f" 2>/dev/null || true)
EOF

  # Generic assignments, excluding obvious placeholders.
  while IFS= read -r line; do
    [ -n "$line" ] || continue
    case "$line" in *qf:allow-secret*) continue ;; esac
    if printf '%s' "$line" | grep -Eiq "$PLACEHOLDER_RE"; then
      continue
    fi
    qf_warn "$f: possible hard-coded credential — $(printf '%s' "$line" | sed 's/^[0-9]*://' | cut -c1-60)"
  done <<EOF
$(grep -niE "$ASSIGN_RE" "$f" 2>/dev/null || true)
EOF
done

if [ "$scanned" -eq 0 ]; then
  qf_info "No changed code/config files to scan."
fi

qf_stage_result secret-scan
