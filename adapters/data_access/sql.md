# SQL Data Access Adapter

## Use For

- Warehouses and relational databases.
- Parameterized analytical queries.
- Point-in-time extracts for research and monitoring.

## Delivery Rules

- Require parameterized queries or reviewed SQL artifacts.
- Capture database, schema, table/view names, row count, and query hash.
- Record transaction isolation or snapshot semantics when available.
- Enforce read-only access for analytical workflows unless a spec approves writes.
- Return data contract evidence for downstream ingestion agents.

## Risks

- Temporal joins can leak future information.
- Unbounded queries can create warehouse cost or performance incidents.
- Credentials and connection strings must remain under secrets management.
