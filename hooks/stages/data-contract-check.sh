#!/bin/sh
# Quant gate - Data contract check.
#
# When a data contract artifact exists, verifies it declares the elements a
# downstream consumer needs: schema, keys, point-in-time rules, and missingness
# thresholds. Advisory by default; set QF_STAGE_ENFORCE=1 to block.

set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DIR/common.sh"

qf_stage_header data-contract "Data contract completeness check"
cd "$QF_ROOT"

contracts=""
for pattern in \
  "data_contract*.md" "*/data_contract*.md" \
  "specs/*/data_contract*.md" "contracts/*.md"; do
  for f in $pattern; do
    case "$f" in
      templates/*|prompts/*) continue ;;
    esac
    [ -f "$f" ] && contracts="$contracts $f"
  done
done

if [ -z "$contracts" ]; then
  qf_info "No data contract found (see templates/data/data_contract.md)."
  qf_stage_result data-contract
  exit $?
fi

check_theme() { # file, label, regex
  if grep -riqE "$3" "$1" 2>/dev/null; then
    qf_info "$(basename "$1"): $2 declared."
  else
    qf_warn "$(basename "$1"): $2 not declared."
  fi
}

for c in $contracts; do
  check_theme "$c" "schema/columns"     "schema|column|field|dtype|type"
  check_theme "$c" "primary/join keys"  "primary key|join key|unique key|key column|grain"
  check_theme "$c" "point-in-time rules" "point.in.time|as.of|availability|publication lag"
  check_theme "$c" "missingness rules"  "missing|null|nan|completeness|coverage"
done

qf_stage_result data-contract
