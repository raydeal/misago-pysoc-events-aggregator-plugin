from django.db import models


class Source(models.Model):
    class Kind(models.TextChoices):
        RSS = "rss", "RSS"
        HTML = "html", "HTML"

    name = models.CharField(max_length=150)
    url = models.URLField(max_length=2048)
    kind = models.CharField(max_length=16, choices=Kind.choices)
    enabled = models.BooleanField(default=True)
    category_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Optional Misago category id. Falls back to PYSOC_EVENTS_CATEGORY_ID.",
    )
    item_selector = models.CharField(
        max_length=255,
        blank=True,
        help_text="CSS selector for each event on an HTML listing page.",
    )
    title_selector = models.CharField(max_length=255, blank=True)
    url_selector = models.CharField(max_length=255, blank=True)
    date_selector = models.CharField(max_length=255, blank=True)
    body_selector = models.CharField(max_length=255, blank=True)
    poll_interval_minutes = models.PositiveIntegerField(default=60)
    last_fetched_at = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class IngestedItem(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PUBLISHED = "published", "Published"
        SKIPPED = "skipped", "Skipped"
        FAILED = "failed", "Failed"

    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="items")
    external_id = models.CharField(max_length=512)
    title = models.CharField(max_length=255)
    canonical_url = models.URLField(max_length=2048)
    payload = models.JSONField(default=dict)
    thread = models.ForeignKey(
        "misago_threads.Thread",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
    )
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "external_id"],
                name="unique_pysoc_source_external_id",
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title
