# Alert Policy Tasks

## Define A Rule

Input: a metric, a condition, and a severity.

Output: an `AlertPolicy` with a dedup key and a rationale for the threshold.

## Evaluate Policies

Input: policies and current monitoring observations.

Output: the fired alerts (`evaluate_policies`) and the expected alert rate.

## Cut Alert Noise

Input: a noisy alert stream.

Output: tuned thresholds, suppression windows, and dedup so real alerts stand out.

## Cover Absence Of Data

Input: a metric whose absence is itself a failure.

Output: a missing-data policy with severity and owner.
