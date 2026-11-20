from misago_pysoc_events_aggregator_plugin.ingest.scrape import parse_html_listing


def test_parse_html_listing_resolves_relative_urls(html_listing):
    events = parse_html_listing(
        html_listing,
        "https://example.com/events",
        item_selector=".event",
        title_selector=".title",
        url_selector=".title",
        date_selector="time",
        body_selector=".desc",
    )
    assert len(events) == 2
    assert events[0].title == "PySoc Lagos"
    assert events[0].canonical_url == "https://example.com/e/1"
    assert events[0].external_id == "https://example.com/e/1"
    assert "local Python social" in events[0].description
    assert events[0].starts_at is not None
    assert events[1].canonical_url == "https://example.com/e/2"


def test_parse_html_listing_requires_item_selector():
    try:
        parse_html_listing("<html></html>", "https://example.com", item_selector="")
    except ValueError as exc:
        assert "item_selector" in str(exc)
    else:
        raise AssertionError("expected ValueError")
