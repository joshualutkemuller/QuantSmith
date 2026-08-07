# Webhook Alert Delivery Adapter

## Use For

- Universal integration fallback.
- Custom internal tools.
- Low-level integration tests.
- Downstream workflow triggers where the target system owns its own delivery.

## Provider Requirements

- Allowlisted URL.
- Secret-managed signing key or bearer token.
- Timeout, retry, and backoff configuration.
- Optional mTLS or IP allowlist for production routes.

## Payload Mapping

Webhook payloads should preserve the channel-neutral contract as JSON with
provider-specific metadata under `provider_context`.

```yaml
provider_context:
  method: POST
  content_type: application/json
  signature_header: string | null
```

## Delivery Rules

- Sign payloads when the receiving system supports signatures.
- Treat non-2xx responses as failures unless the route declares otherwise.
- Use idempotency keys from `correlation_id` and `dedupe_key`.
- Do not follow redirects in production unless explicitly allowlisted.
- Enforce a strict timeout to prevent workflow hangs.

## Result Evidence

Capture HTTP status, response correlation ID, redacted response body hash, and
retryability classification.
