#!/bin/sh
# Stage 4 - Testing & Validation gate.
#
# Encourages that code changes are accompanied by tests and runs the test suite
# when a runner is available. Advisory by default.

set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DIR/common.sh"

qf_stage_header testing "Test presence & execution check"
cd "$QF_ROOT"

changed=$(qf_changed_files)

# Did source change without any test change?
src_changed=0
test_changed=0
for f in $changed; do
  case "$f" in
    */test_*.py|*_test.py|tests/*|*/tests/*|test/*|*/test/*|*.test.js|*.spec.js|*.spec.ts)
      test_changed=1 ;;
    *.py|*.js|*.ts|*.go|*.rs|*.java)
      src_changed=1 ;;
  esac
done

if [ "$src_changed" -eq 1 ] && [ "$test_changed" -eq 0 ]; then
  qf_warn "Source changed but no test files changed (see agents/testing_validation)."
elif [ "$src_changed" -eq 1 ]; then
  qf_info "Source and tests changed together."
fi

# Run tests only when explicitly enabled, since suites can be slow.
if [ "${QF_RUN_TESTS:-0}" = "1" ]; then
  if [ -f "pyproject.toml" ] || [ -f "setup.cfg" ] || [ -d "tests" ]; then
    if command -v pytest >/dev/null 2>&1; then
      if ! pytest -q >/dev/null 2>&1; then
        qf_warn "pytest reported failures."
      else
        qf_info "pytest passed."
      fi
    else
      qf_info "pytest not installed; skipping test run."
    fi
  else
    qf_info "No Python test layout detected; skipping test run."
  fi
else
  qf_info "Test execution disabled (set QF_RUN_TESTS=1 to run the suite)."
fi

qf_stage_result testing
