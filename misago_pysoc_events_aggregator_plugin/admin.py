from django.contrib import admin

from .models import IngestedItem, Source


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "kind",
        "enabled",
        "poll_interval_minutes",
        "last_fetched_at",
        "url",
    )
    list_filter = ("kind", "enabled")
    search_fields = ("name", "url")
    fieldsets = (
        (None, {"fields": ("name", "url", "kind", "enabled", "category_id")}),
        (
            "HTML scrape selectors",
            {
                "classes": ("collapse",),
                "fields": (
                    "item_selector",
                    "title_selector",
                    "url_selector",
                    "date_selector",
                    "body_selector",
                ),
            },
        ),
        (
            "Polling",
            {"fields": ("poll_interval_minutes", "last_fetched_at", "last_error")},
        ),
    )
    readonly_fields = ("last_fetched_at", "last_error")


@admin.register(IngestedItem)
class IngestedItemAdmin(admin.ModelAdmin):
    list_display = ("title", "source", "status", "canonical_url", "created_at")
    list_filter = ("status", "source")
    search_fields = ("title", "canonical_url", "external_id")
    readonly_fields = (
        "source",
        "external_id",
        "title",
        "canonical_url",
        "payload",
        "thread",
        "created_at",
        "updated_at",
    )
