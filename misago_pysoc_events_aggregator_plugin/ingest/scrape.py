from __future__ import annotations

from urllib.parse import urljoin

from selectolax.lexbor import LexborHTMLParser

from .normalize import html_to_text, normalize_event
from .types import NormalizedEvent


def _node_text(node) -> str:
    if node is None:
        return ""
    return html_to_text(node.text(separator=" "))


def _node_url(node, base_url: str) -> str:
    if node is None:
        return ""
    href = node.attributes.get("href") or node.attributes.get("src") or ""
    if not href:
        href = _node_text(node)
    href = href.strip()
    if not href:
        return ""
    return urljoin(base_url, href)


def _node_datetime(node) -> str:
    if node is None:
        return ""
    return (
        node.attributes.get("datetime")
        or node.attributes.get("content")
        or _node_text(node)
    )


def parse_html_listing(
    html: str,
    base_url: str,
    *,
    item_selector: str,
    title_selector: str = "",
    url_selector: str = "",
    date_selector: str = "",
    body_selector: str = "",
) -> list[NormalizedEvent]:
    if not item_selector:
        raise ValueError("HTML sources require an item_selector")

    tree = LexborHTMLParser(html)
    events: list[NormalizedEvent] = []
    for item in tree.css(item_selector):
        title_node = item.css_first(title_selector) if title_selector else item
        url_node = item.css_first(url_selector) if url_selector else title_node
        date_node = item.css_first(date_selector) if date_selector else None
        body_node = item.css_first(body_selector) if body_selector else None

        title = _node_text(title_node)
        url = _node_url(url_node, base_url)
        event = normalize_event(
            external_id=url,
            title=title,
            canonical_url=url,
            description=_node_text(body_node),
            starts_at=_node_datetime(date_node),
            payload={"source_kind": "html"},
        )
        if event:
            events.append(event)
    return events
