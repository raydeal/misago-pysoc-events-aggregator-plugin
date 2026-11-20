from misago_pysoc_events_aggregator_plugin.ingest.rss import parse_rss


def test_parse_rss_extracts_entries(rss_sample):
    events = parse_rss(rss_sample)
    assert len(events) == 2
    assert events[0].title == "Django meetup"
    assert events[0].canonical_url == "https://example.com/events/django"
    assert events[0].external_id == "https://example.com/events/django"
    assert "Django people" in events[0].description
    assert events[0].starts_at is not None


def test_parse_rss_uses_guid_when_different_from_link(rss_sample):
    events = parse_rss(rss_sample)
    pysoc = events[1]
    assert pysoc.external_id == "pysoc-evening-1"
    assert pysoc.canonical_url == "https://example.com/events/pysoc"
    assert "Board games" in pysoc.description
