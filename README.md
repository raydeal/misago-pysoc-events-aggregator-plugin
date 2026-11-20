# misago-pysoc-events-aggregator-plugin

![Test workflow](https://github.com/raydeal/misago-pysoc-events-aggregator-plugin/actions/workflows/tests.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/raydeal/misago-pysoc-events-aggregator-plugin/badge.svg?branch=main)](https://coveralls.io/github/raydeal/misago-pysoc-events-aggregator-plugin?branch=main)
![Works on Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)

Misago plugin that collects Python social events from RSS feeds and HTML listing pages, then publishes each new event as a forum thread. Built for [python-forum.pl](https://python-forum.pl).

The layout follows Misago’s plugin rules from [misago-pypi-plugin](https://github.com/rafalp/misago-pypi-plugin) (PyPI package + `misago_plugin.py` manifest) and [misago-users-online-plugin](https://github.com/rafalp/misago-users-online-plugin) (Django `AppConfig`, models, management command).

## Install

The import name must stay `misago_pysoc_events_aggregator_plugin` (PyPI name with hyphens replaced by underscores).

### From the filesystem

Clone this repository into your Misago `plugins/` directory:

```text
plugins/misago-pysoc-events-aggregator-plugin/
  misago_pysoc_events_aggregator_plugin/
    misago_plugin.py
```

Rebuild the Docker image (`./dev rebuild` locally, or `./appctl rebuild` on [misago-docker](https://github.com/rafalp/misago-docker)).

### From PyPI

Add this line to `plugins/pip-install.txt` and rebuild:

```text
misago-pysoc-events-aggregator-plugin
```

## Configure

In Django settings:

```python
PYSOC_EVENTS_CATEGORY_ID = 12  # category that receives event threads
PYSOC_EVENTS_POSTER_ID = 3     # bot/user that starts the threads
# optional
PYSOC_EVENTS_USER_AGENT = "Misago-PySoc-Events-Aggregator/0.1"
PYSOC_EVENTS_REQUEST_TIMEOUT = 20
PYSOC_EVENTS_REQUEST_DELAY = 1
```

Run migrations, then add sources in Django admin (`Source`):

- **RSS:** set kind to RSS and paste the feed URL.
- **HTML:** set kind to HTML and fill CSS selectors (`item_selector` is required; `title_selector`, `url_selector`, `date_selector`, `body_selector` are relative to each item).

## Run

```bash
python manage.py aggregate_pysoc_events
```

Useful flags:

- `--force` — ignore poll intervals
- `--dry-run` — fetch and parse without writing
- `--no-publish` — ingest only, do not create threads

Example cron (hourly):

```cron
0 * * * * /path/to/python manage.py aggregate_pysoc_events
```

Duplicate events are skipped using a unique `(source, external_id)` key (RSS GUID or canonical URL).

## Tests

```bash
pip install -e ".[test]"
pytest
```

Parser tests do not require a running Misago site.
