#!/bin/sh
# Stage 5 - Deployment & Release gate.
#
# Checks for the release artifacts a safe deployment needs: a production
# readiness checklist, a rollback/kill-switch plan, and release notes.
# Advisory by default.

set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DIR/common.sh"

qf_stage_header deployment "Release readiness check"
cd "$QF_ROOT"

# Production readiness checklist.
if qf_glob_exists "production_readiness*.md" "docs/production_readiness*.md" \
      "templates/docs/production_readiness*.md"; then
  qf_info "Production readiness checklist present."
else
  qf_warn "No production readiness checklist found (see agents/deployment_release)."
fi

# Rollback / kill-switch plan.
if grep -riq -e "rollback" -e "kill switch" -e "kill-switch" . --include="*.md" 2>/dev/null; then
  qf_info "Rollback / kill-switch plan referenced."
else
  qf_warn "No rollback or kill-switch plan found in docs."
fi

# Release notes / changelog.
if qf_glob_exists "CHANGELOG*" "release_notes*.md" "docs/release_notes*.md"; then
  qf_info "Release notes / changelog present."
else
  qf_warn "No release notes or CHANGELOG found."
fi

qf_stage_result deployment
