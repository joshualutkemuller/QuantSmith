#!/bin/sh
# Memory gate - workflow memory structure & safety check.
#
# Validates the persistent workflow memory store (memory/): that records carry
# provenance, and that memory contains no secrets, connection strings, or PII
# (memory is metadata only). See instructions/workflow_memory.md and
# specs/0002-workflow-memory/. Advisory by default; QF_STAGE_ENFORCE=1 blocks.

set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DIR/common.sh"

qf_stage_header memory "Workflow memory structure & safety check"
cd "$QF_ROOT"

if [ ! -d memory ]; then
  qf_info "No memory/ store; workflow-memory checks skipped."
  qf_stage_result memory
  exit $?
fi

# Manifest.
if [ -f memory/manifest.yaml ]; then
  qf_info "Memory manifest present."
else
  qf_warn "No memory/manifest.yaml (see instructions/workflow_memory.md)."
fi

# Provenance: every record catalog must declare the required fields.
records=$(find memory -type f \( -name provenance.yaml -o -name index.yaml \) 2>/dev/null)
if [ -z "$records" ]; then
  qf_warn "No memory records found (provenance.yaml / index.yaml)."
else
  for r in $records; do
    for field in first_seen last_confirmed access_level; do
      grep -q "$field" "$r" 2>/dev/null || qf_warn "$r: records missing '$field'"
    done
  done
fi

# Safety scan: memory is metadata only — no secrets, connection strings, or PII.
CONN_RE='[A-Za-z][A-Za-z0-9+.-]*://[^:@/[:space:]]+:[^@/[:space:]]+@'
CRED_RE='(password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key)["'"'"' ]*[:=][[:space:]]*["'"'"']?[A-Za-z0-9/+_-]{8,}'
KEY_RE='-----BEGIN [A-Z ]*PRIVATE KEY-----'
EMAIL_RE='[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
SSN_RE='[0-9]{3}-[0-9]{2}-[0-9]{4}'

for f in $(find memory -type f \( -name '*.md' -o -name '*.yaml' -o -name '*.yml' -o -name '*.txt' \) 2>/dev/null); do
  grep -Eq "$CONN_RE" "$f" 2>/dev/null && qf_warn "$f: possible connection string with credentials in memory"
  grep -Eiq "$CRED_RE" "$f" 2>/dev/null && qf_warn "$f: possible credential value in memory"
  grep -Eq "$KEY_RE" "$f" 2>/dev/null && qf_warn "$f: private key in memory"
  grep -Eq "$EMAIL_RE" "$f" 2>/dev/null && qf_warn "$f: possible PII (email) in memory"
  grep -Eq "$SSN_RE" "$f" 2>/dev/null && qf_warn "$f: possible PII (SSN-like) in memory"
done

[ "$QF_FINDINGS" -eq 0 ] && qf_info "Memory store structure and safety OK."
qf_stage_result memory
