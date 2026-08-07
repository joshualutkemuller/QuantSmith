# Email Attachment Artifact Delivery Adapter

## Use For

- Sending approved reports or draft packs to a known recipient group.
- Attaching compact evidence bundles.
- Linking to larger artifacts stored elsewhere.

## Delivery Rules

- Prefer links over attachments for large, sensitive, or frequently updated
  artifacts.
- Enforce attachment size and classification policy.
- Include artifact type, workflow ID, run ID, as-of timestamp, and owner.
- Use the email alert adapter for the actual send and record both artifact and
  message evidence.

## Risks

- Forwarding can bypass intended access controls.
- Attachments create stale copies.
- Large files can fail silently or be blocked by enterprise mail policy.
