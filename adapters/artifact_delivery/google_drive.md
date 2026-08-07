# Google Drive Artifact Delivery Adapter

## Use For

- Shared documents, reports, spreadsheets, and presentation-ready artifacts.
- Team-readable evidence bundles.
- Persistent draft packs that need comments or follow-up.

## Delivery Rules

- Map `visibility` and `classification` to a Drive folder and sharing policy.
- Store generated artifacts in a workflow-specific folder.
- Preserve workflow ID, run ID, artifact type, and as-of timestamp in metadata.
- Do not publish restricted artifacts to broadly shared folders.
- Return the Drive file ID and shareable URI when allowed.

## Risks

- Folder inheritance can broaden access unexpectedly.
- External sharing must be explicitly approved.
- Versioned artifacts need naming and retention discipline.
