from django.conf import settings as django_settings

DEFAULT_USER_AGENT = "Misago-PySoc-Events-Aggregator/0.1"
DEFAULT_TIMEOUT = 20.0
DEFAULT_DELAY_SECONDS = 1.0


class PluginSettingsError(RuntimeError):
    pass


def get_category_id() -> int:
    value = getattr(django_settings, "PYSOC_EVENTS_CATEGORY_ID", None)
    if not value:
        raise PluginSettingsError(
            "Set PYSOC_EVENTS_CATEGORY_ID to the Misago category id for new event threads."
        )
    return int(value)


def get_poster_id() -> int:
    value = getattr(django_settings, "PYSOC_EVENTS_POSTER_ID", None)
    if not value:
        raise PluginSettingsError(
            "Set PYSOC_EVENTS_POSTER_ID to the user id that should start event threads."
        )
    return int(value)


def get_user_agent() -> str:
    return getattr(django_settings, "PYSOC_EVENTS_USER_AGENT", DEFAULT_USER_AGENT)


def get_timeout() -> float:
    return float(getattr(django_settings, "PYSOC_EVENTS_REQUEST_TIMEOUT", DEFAULT_TIMEOUT))


def get_request_delay() -> float:
    return float(
        getattr(django_settings, "PYSOC_EVENTS_REQUEST_DELAY", DEFAULT_DELAY_SECONDS)
    )
