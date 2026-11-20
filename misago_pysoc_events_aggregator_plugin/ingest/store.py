from __future__ import annotations

from .types import NormalizedEvent


def item_defaults(event: NormalizedEvent) -> dict:
    return {
        "title": event.title[:255],
        "canonical_url": event.canonical_url[:2048],
        "payload": event.to_payload(),
        "status": "pending",
    }


def upsert_events(source, events: list[NormalizedEvent]) -> tuple[int, int]:
    from ..models import IngestedItem

    created_count = 0
    seen_count = 0
    for event in events:
        _item, created = IngestedItem.objects.get_or_create(
            source=source,
            external_id=event.external_id[:512],
            defaults=item_defaults(event),
        )
        if created:
            created_count += 1
        else:
            seen_count += 1
    return created_count, seen_count
