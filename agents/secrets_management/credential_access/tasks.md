# Credential Access Tasks

## Safe Retrieval

Input: the secret(s)/keys to read and the consuming code.

Output: a retrieval implementation using env injection or a store client, with
least-privilege identity and leak guards.

## Access Path Review

Input: existing secret-reading code.

Output: review of hard-coded secrets, logging/serialization leaks, caching, and
scope, with fixes.

## Remove Hard-Coded Secrets

Input: code with embedded keys or credentials.

Output: refactor to runtime retrieval, plus rotation of the previously embedded
secret and a note to purge it from history.

## Dev/Prod Parity

Input: differing local and production access patterns.

Output: a single, documented retrieval pattern that works safely in both.
