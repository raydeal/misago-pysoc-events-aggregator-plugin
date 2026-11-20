from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def rss_sample() -> str:
    return (FIXTURES / "rss_sample.xml").read_text(encoding="utf-8")


@pytest.fixture
def html_listing() -> str:
    return (FIXTURES / "html_listing.html").read_text(encoding="utf-8")
