from django.apps import AppConfig


class MisagoPysocEventsAggregatorPluginConfig(AppConfig):
    default = True
    default_auto_field = "django.db.models.BigAutoField"
    name = "misago_pysoc_events_aggregator_plugin"
    verbose_name = "PySoc Events Aggregator"
