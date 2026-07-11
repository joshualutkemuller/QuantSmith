#!/bin/sh
# Quant gate - Look-ahead & leakage code-smell check.
#
# Scans changed Python and notebook files for the highest-signal leakage smells
# from instructions/point_in_time.md. Heuristic and advisory by default: it
# points a reviewer at lines to check, it does not prove leakage.
# Set QF_STAGE_ENFORCE=1 to block.

set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DIR/common.sh"

qf_stage_header leakage "Look-ahead & leakage smell check"
cd "$QF_ROOT"

changed=$(qf_changed_files)
scanned=0

for f in $changed; do
  case "$f" in
    *.py|*.ipynb) ;;
    *) continue ;;
  esac
  [ -f "$f" ] || continue
  scanned=$((scanned + 1))

  # Negative shift pulls future values into the present.
  if grep -nE '\.shift\(\s*-' "$f" >/dev/null 2>&1; then
    qf_warn "$f: negative .shift() — pulls future data into the present."
  fi

  # Backfill fills gaps with later observations.
  if grep -nE '\.bfill\(|fillna\([^)]*bfill|method\s*=\s*["'"'"']bfill' "$f" >/dev/null 2>&1; then
    qf_warn "$f: backfill (bfill) — may fill values with future observations."
  fi

  # Time-series split without disabling shuffle.
  if grep -nE 'train_test_split\(' "$f" >/dev/null 2>&1; then
    if ! grep -nE 'shuffle\s*=\s*False' "$f" >/dev/null 2>&1; then
      qf_warn "$f: train_test_split without shuffle=False — verify time-ordered split."
    fi
  fi

  # Scaler fit on what may be the full sample (fit before an explicit split).
  if grep -nE '(StandardScaler|MinMaxScaler|RobustScaler|scaler)\.fit(_transform)?\(' "$f" >/dev/null 2>&1; then
    qf_info "$f: scaler fit present — confirm it is fit on training data only."
  fi
done

if [ "$scanned" -eq 0 ]; then
  qf_info "No changed Python/notebook files to scan."
fi

qf_stage_result leakage
