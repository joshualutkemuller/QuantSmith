# Knowledge Retrieval Tasks

## Answer From Knowledge Base

Input: a user question and the asker's access level.

Output: a grounded, cited answer using only access-permitted sources, with a
confidence and freshness note.

## Access-Scoped Retrieval

Input: a query and an information-barrier context.

Output: results filtered to the asker's authorization, with restricted material
withheld (and not confirmed).

## Freshness Check

Input: a topic and its supporting sources.

Output: how current the answer is, with stale or superseded sources flagged.

## Gap Response

Input: a question the base does not cover.

Output: an explicit "not found" with suggested owners or sources to consult.
