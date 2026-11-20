from __future__ import annotations

from datetime import datetime, timedelta

from .http import fetch_url
from .rss import parse_rss
from .scrape import parse_html_listing
from .store import upsert_events
from .types import NormalizedEvent


def should_fetch(source, now: datetime | None = None, *, force: bool = False) -> bool:
    if force or source.last_fetched_at is None:
        return True
    if now is None:
        from django.utils import timezone

        now = timezone.now()
    interval = timedelta(minutes=source.poll_interval_minutes or 0)
    return now >= source.last_fetched_at + interval


def parse_source(source, content: str) -> list[NormalizedEvent]:
    if source.kind == "rss":
        return parse_rss(content)
    if source.kind == "html":
        return parse_html_listing(
            content,
            source.url,
            item_selector=source.item_selector,
            title_selector=source.title_selector,
            url_selector=source.url_selector,
            date_selector=source.date_selector,
            body_selector=source.body_selector,
        )
    raise ValueError(f"Unsupported source kind: {source.kind}")


def ingest_source(source, *, force: bool = False, dry_run: bool = False) -> dict:
    if not should_fetch(source, force=force):
        return {"skipped": True, "created": 0, "seen": 0, "events": 0}

    content = fetch_url(source.url, check_robots=True)
    events = parse_source(source, content)
    created = 0
    seen = 0
    if not dry_run:
        from django.utils import timezone

        created, seen = upsert_events(source, events)
        source.last_fetched_at = timezone.now()
        source.last_error = ""
        source.save(update_fields=["last_fetched_at", "last_error", "updated_at"])
    return {
        "skipped": False,
        "created": created,
        "seen": seen,
        "events": len(events),
    }
