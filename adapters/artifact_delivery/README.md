# Artifact Delivery Adapters

Artifact delivery adapters persist and distribute workflow outputs such as run
cards, reports, data contracts, model cards, monitoring plans, chart specs, and
content draft packs.

## Files

| File | Purpose |
| --- | --- |
| `adapter_contract.md` | Channel-neutral artifact storage and delivery schema. |
| `local_file.md` | Local or repository-backed artifact output. |
| `email_attachment.md` | Email links or attachments for approved artifacts. |
| `google_drive.md` | Google Drive or shared-drive publishing. |
| `notion.md` | Notion page/database publishing. |

## Design Rule

The workflow owns artifact content and approval. The adapter owns destination
format, provider metadata, permissions, and evidence of delivery.
