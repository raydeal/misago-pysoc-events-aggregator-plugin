from __future__ import annotations

import time
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import httpx


class RobotsDisallowed(RuntimeError):
    pass


def robots_url_for(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}/robots.txt"


def robots_allowed(client: httpx.Client, url: str, user_agent: str) -> bool:
    robots_url = robots_url_for(url)
    try:
        response = client.get(robots_url)
        if response.status_code >= 400:
            return True
        parser = RobotFileParser()
        parser.parse(response.text.splitlines())
        return parser.can_fetch(user_agent, url)
    except httpx.HTTPError:
        return True


def fetch_url(url: str, *, check_robots: bool = True) -> str:
    from misago_pysoc_events_aggregator_plugin.tests.settings import get_request_delay, get_timeout, get_user_agent

    user_agent = get_user_agent()
    timeout = get_timeout()
    headers = {"User-Agent": user_agent, "Accept": "*/*"}
    with httpx.Client(
        headers=headers,
        timeout=timeout,
        follow_redirects=True,
    ) as client:
        if check_robots and not robots_allowed(client, url, user_agent):
            raise RobotsDisallowed(f"robots.txt disallows fetching {url}")
        response = client.get(url)
        response.raise_for_status()
        body = response.text
    delay = get_request_delay()
    if delay > 0:
        time.sleep(delay)
    return body


def absolutize(base_url: str, href: str) -> str:
    return urljoin(base_url, href)
