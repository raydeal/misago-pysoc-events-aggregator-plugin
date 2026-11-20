from datetime import datetime, timezone
from types import SimpleNamespace

from misago_pysoc_events_aggregator_plugin.ingest.normalize import (
    html_to_text,
    normalize_event,
)
from misago_pysoc_events_aggregator_plugin.ingest.pipeline import should_fetch
from misago_pysoc_events_aggregator_plugin.ingest.store import item_defaults


def test_html_to_text_strips_tags():
    assert html_to_text("<p>Hello <strong>world</strong></p>") == "Hello world"


def test_normalize_event_rejects_empty_title():
    assert (
        normalize_event(
            external_id="x",
            title="   ",
            canonical_url="https://example.com/x",
        )
        is None
    )


def test_item_defaults_include_pending_status():
    event = normalize_event(
        external_id="abc",
        title="Meetup",
        canonical_url="https://example.com/meetup",
        description="Bring snacks",
    )
    defaults = item_defaults(event)
    assert defaults["status"] == "pending"
    assert defaults["title"] == "Meetup"
    assert defaults["payload"]["description"] == "Bring snacks"


def test_should_fetch_respects_interval():
    now = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    source = SimpleNamespace(
        last_fetched_at=datetime(2024, 1, 1, 11, 30, tzinfo=timezone.utc),
        poll_interval_minutes=60,
    )
    assert should_fetch(source, now) is False
    assert should_fetch(source, now, force=True) is True
    source.last_fetched_at = None
    assert should_fetch(source, now) is True
