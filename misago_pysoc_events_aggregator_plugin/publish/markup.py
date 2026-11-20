from __future__ import annotations

from datetime import datetime


def _format_when(value) -> str:
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M")
    if isinstance(value, str) and value:
        return value
    return ""


def render_event_markup(item) -> str:
    payload = getattr(item, "payload", None) or {}
    lines = [item.title, ""]
    when = _format_when(payload.get("starts_at"))
    if when:
        lines.append(f"**When:** {when}")
    location = payload.get("location") or ""
    if location:
        lines.append(f"**Where:** {location}")
    source_name = getattr(getattr(item, "source", None), "name", "") or payload.get("source_name") or ""
    if source_name:
        lines.append(f"**Source:** {source_name}")
    if item.canonical_url:
        lines.append(f"**Link:** {item.canonical_url}")
    description = payload.get("description") or ""
    if description:
        lines.extend(["", description])
    if item.canonical_url:
        lines.extend(["", f"Original listing: <{item.canonical_url}>"])
    return "\n".join(lines).strip() + "\n"


def thread_plugin_data(item) -> dict:
    return {
        "pysoc_events": {
            "source_id": getattr(item, "source_id", None)
            or getattr(getattr(item, "source", None), "id", None),
            "canonical_url": item.canonical_url,
            "external_id": item.external_id,
        }
    }
