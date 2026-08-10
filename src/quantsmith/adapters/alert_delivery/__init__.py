"""Executable alert-delivery providers (spec 0032).

Construct and, given an injected transport, send an alert delivery event:
``deliver_email`` and ``deliver_webhook``, per ``adapters/alert_delivery/
adapter_contract.md``. Standard-library only; ``dry_run=True`` (the default)
never performs I/O.
"""

from __future__ import annotations

from .email import build_email_payload, deliver_email
from .result import (
    AlertDeliveryEvent,
    Acknowledgement,
    DeliveryResult,
    EvidenceItem,
    Privacy,
    Transport,
    TransportError,
    assert_no_secret,
    contains_secret,
    redact_text,
)
from .webhook import build_webhook_payload, deliver_webhook

__all__ = [
    "Acknowledgement",
    "AlertDeliveryEvent",
    "DeliveryResult",
    "EvidenceItem",
    "Privacy",
    "Transport",
    "TransportError",
    "assert_no_secret",
    "build_email_payload",
    "build_webhook_payload",
    "contains_secret",
    "deliver_email",
    "deliver_webhook",
    "redact_text",
]
