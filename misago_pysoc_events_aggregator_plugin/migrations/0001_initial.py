import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("misago_threads", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Source",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150)),
                ("url", models.URLField(max_length=2048)),
                (
                    "kind",
                    models.CharField(
                        choices=[("rss", "RSS"), ("html", "HTML")],
                        max_length=16,
                    ),
                ),
                ("enabled", models.BooleanField(default=True)),
                (
                    "category_id",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Optional Misago category id. Falls back to PYSOC_EVENTS_CATEGORY_ID.",
                        null=True,
                    ),
                ),
                (
                    "item_selector",
                    models.CharField(
                        blank=True,
                        help_text="CSS selector for each event on an HTML listing page.",
                        max_length=255,
                    ),
                ),
                ("title_selector", models.CharField(blank=True, max_length=255)),
                ("url_selector", models.CharField(blank=True, max_length=255)),
                ("date_selector", models.CharField(blank=True, max_length=255)),
                ("body_selector", models.CharField(blank=True, max_length=255)),
                ("poll_interval_minutes", models.PositiveIntegerField(default=60)),
                ("last_fetched_at", models.DateTimeField(blank=True, null=True)),
                ("last_error", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="IngestedItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("external_id", models.CharField(max_length=512)),
                ("title", models.CharField(max_length=255)),
                ("canonical_url", models.URLField(max_length=2048)),
                ("payload", models.JSONField(default=dict)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("published", "Published"),
                            ("skipped", "Skipped"),
                            ("failed", "Failed"),
                        ],
                        default="pending",
                        max_length=16,
                    ),
                ),
                ("error", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="misago_pysoc_events_aggregator_plugin.source",
                    ),
                ),
                (
                    "thread",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="misago_threads.thread",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddConstraint(
            model_name="ingesteditem",
            constraint=models.UniqueConstraint(
                fields=("source", "external_id"),
                name="unique_pysoc_source_external_id",
            ),
        ),
    ]
