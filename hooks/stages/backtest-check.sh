#!/bin/sh
# Quant gate - Backtest integrity check.
#
# When a backtest report artifact exists, verifies it addresses the integrity
# themes that separate real edge from overfit: transaction costs, true
# out-of-sample, benchmark, turnover/capacity, and multiple-testing correction.
# If the backtest involves short positions, it must also address financing
# (borrow cost and short rebate). Advisory by default; QF_STAGE_ENFORCE=1 blocks.

set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DIR/common.sh"

qf_stage_header backtest "Backtest integrity check"
cd "$QF_ROOT"

# Find backtest *report/result* artifacts (exclude templates and this SDK's own
# prompt/agent scaffolding to avoid false positives).
reports=""
for pattern in \
  "backtest_report*.md" "*_backtest_report.md" \
  "docs/backtest_report*.md" "specs/*/backtest*.md" \
  "reports/*backtest*.md" "backtest_result*.md"; do
  for f in $pattern; do
    case "$f" in
      templates/*|prompts/*) continue ;;
    esac
    [ -f "$f" ] && reports="$reports $f"
  done
done

if [ -z "$reports" ]; then
  qf_info "No backtest report artifact detected (see templates/docs/backtest_report.md)."
  qf_stage_result backtest
  exit $?
fi

check_theme() { # file, label, regex
  if grep -riqE "$3" "$1" 2>/dev/null; then
    qf_info "$(basename "$1"): $2 addressed."
  else
    qf_warn "$(basename "$1"): $2 not addressed."
  fi
}

check_theme_if() { # file, trigger_regex, label, regex
  if grep -riqE "$2" "$1" 2>/dev/null; then
    check_theme "$1" "$3" "$4"
  fi
}

for r in $reports; do
  check_theme "$r" "transaction costs" "transaction cost|slippage|commission|borrow"
  check_theme "$r" "out-of-sample"     "out.of.sample|oos|walk.forward|holdout"
  check_theme "$r" "benchmark"         "benchmark|baseline"
  check_theme "$r" "turnover/capacity" "turnover|capacity"
  check_theme "$r" "multiple testing"  "multiple.testing|deflated|probabilistic sharpe|psr|p.hack"
  # Only required when the backtest involves shorts: financing must be accounted for.
  check_theme_if "$r" "short.sell|short.selling|shorts?[^a-z]|long.short" \
    "financing (borrow cost / short rebate)" \
    "borrow|short rebate|rebate|stock loan|financing cost|hard.to.borrow"
done

qf_stage_result backtest
