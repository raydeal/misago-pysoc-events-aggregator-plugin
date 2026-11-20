from types import SimpleNamespace

from misago_pysoc_events_aggregator_plugin.ingest.http import (
    robots_allowed,
    robots_url_for,
)


class FakeResponse:
    def __init__(self, text: str, status_code: int = 200):
        self.text = text
        self.status_code = status_code


def test_robots_url_for():
    assert robots_url_for("https://example.com/events/list") == "https://example.com/robots.txt"


def test_robots_allowed_honors_disallow():
    robots = "User-agent: *\nDisallow: /private\n"
    client = SimpleNamespace(get=lambda url: FakeResponse(robots))
    assert robots_allowed(client, "https://example.com/events", "*") is True
    assert robots_allowed(client, "https://example.com/private/secret", "*") is False


def test_missing_robots_txt_allows_fetch():
    client = SimpleNamespace(get=lambda url: FakeResponse("", status_code=404))
    assert robots_allowed(client, "https://example.com/events", "*") is True
