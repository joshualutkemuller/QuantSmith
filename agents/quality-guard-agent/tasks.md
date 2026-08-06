# Quality Guard Agent Tasks

## Contract Validation

Input: a pipeline output and its contract.

Output: schema/contract validation results.

## Policy Check

Input: an output and the policy rules.

Output: PII, metric-definition, and naming compliance findings.

## Confidence Scoring

Input: validation and policy results.

Output: a confidence score with blocking vs non-blocking issues.

## Stage Decision

Input: the scored results.

Output: an approve/reject decision with remediation for blockers.
