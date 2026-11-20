from types import SimpleNamespace

from misago_pysoc_events_aggregator_plugin.publish.markup import (
    render_event_markup,
    thread_plugin_data,
)


def test_render_event_markup_includes_title_and_link():
    item = SimpleNamespace(
        title="Django meetup",
        canonical_url="https://example.com/events/django",
        source=SimpleNamespace(name="Example RSS"),
        payload={
            "starts_at": "2024-01-01T12:00:00+00:00",
            "location": "Lagos",
            "description": "Come hang out.",
        },
    )
    markup = render_event_markup(item)
    assert "Django meetup" in markup
    assert "**When:**" in markup
    assert "**Where:** Lagos" in markup
    assert "https://example.com/events/django" in markup
    assert "Come hang out." in markup


def test_thread_plugin_data_stores_source_and_url():
    item = SimpleNamespace(
        source_id=4,
        canonical_url="https://example.com/e/1",
        external_id="https://example.com/e/1",
        source=SimpleNamespace(id=4),
    )
    data = thread_plugin_data(item)
    assert data["pysoc_events"]["source_id"] == 4
    assert data["pysoc_events"]["canonical_url"] == "https://example.com/e/1"
