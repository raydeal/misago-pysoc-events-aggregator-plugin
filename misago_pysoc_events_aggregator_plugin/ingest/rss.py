from __future__ import annotations

from datetime import datetime, timezone

import feedparser

from .normalize import normalize_event
from .types import NormalizedEvent


def _entry_description(entry) -> str:
    if entry.get("summary"):
        return entry.summary
    content = entry.get("content") or []
    if content and content[0].get("value"):
        return content[0]["value"]
    return entry.get("description") or ""


def _entry_datetime(entry) -> datetime | None:
    for key in ("published_parsed", "updated_parsed"):
        parsed = entry.get(key)
        if parsed:
            return datetime(*parsed[:6], tzinfo=timezone.utc)
    return None


def parse_rss(content: str | bytes) -> list[NormalizedEvent]:
    parsed = feedparser.parse(content)
    events: list[NormalizedEvent] = []
    for entry in parsed.entries:
        link = (entry.get("link") or "").strip()
        guid = (entry.get("id") or link).strip()
        title = (entry.get("title") or "").strip()
        event = normalize_event(
            external_id=guid or link,
            title=title,
            canonical_url=link or guid,
            description=_entry_description(entry),
            starts_at=_entry_datetime(entry),
            payload={"source_kind": "rss"},
        )
        if event:
            events.append(event)
    return events
