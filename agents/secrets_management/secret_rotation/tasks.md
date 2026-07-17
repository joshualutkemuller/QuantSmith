# Secret Rotation Tasks

## Zero-Downtime Rotation

Input: a live credential/key and its consumers.

Output: an ordered rotation sequence (issue → propagate → cutover → revoke) with
versioning that avoids downtime.

## Rotation Policy

Input: a set of secrets and compliance/cadence needs.

Output: per-secret rotation cadence, ownership, and automation recommendations.

## Leaked-Secret Response

Input: a secret suspected or known to be exposed.

Output: an immediate rotate-revoke sequence and an incident record, plus history
purge guidance.

## Create/Update Custom Keys

Input: new or changed custom key/value entries.

Output: a write procedure targeting the store with versioning and access scope,
never committing values.
