from __future__ import annotations

import re
from datetime import datetime
from html import unescape

from dateutil import parser as date_parser
from selectolax.lexbor import LexborHTMLParser

from .types import NormalizedEvent

_WHITESPACE_RE = re.compile(r"\s+")


def html_to_text(value: str | None) -> str:
    if not value:
        return ""
    tree = LexborHTMLParser(value)
    text = tree.text(separator=" ")
    return collapse_whitespace(unescape(text))


def collapse_whitespace(value: str) -> str:
    return _WHITESPACE_RE.sub(" ", value).strip()


def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return date_parser.parse(value, fuzzy=True)
    except (ValueError, OverflowError, TypeError):
        return None


def normalize_event(
    *,
    external_id: str,
    title: str,
    canonical_url: str,
    description: str = "",
    starts_at: datetime | str | None = None,
    location: str = "",
    payload: dict | None = None,
) -> NormalizedEvent | None:
    title = html_to_text(title) if "<" in title else collapse_whitespace(title)
    canonical_url = collapse_whitespace(canonical_url)
    external_id = collapse_whitespace(external_id) or canonical_url
    if not title or not external_id:
        return None
    if isinstance(starts_at, str):
        starts_at = parse_datetime(starts_at)
    return NormalizedEvent(
        external_id=external_id[:512],
        title=title[:255],
        canonical_url=canonical_url[:2048],
        description=html_to_text(description) if description and "<" in description else collapse_whitespace(description),
        starts_at=starts_at,
        location=collapse_whitespace(location),
        payload=payload or {},
    )
