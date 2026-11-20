from __future__ import annotations

from django.db import transaction
from django.db.models import F

from ..models import IngestedItem
from misago_pysoc_events_aggregator_plugin.tests.settings import get_category_id, get_poster_id
from .markup import render_event_markup, thread_plugin_data


def publish_item(item: IngestedItem):
    from misago.categories.models import Category
    from misago.parser.parse import parse
    from misago.threads.checksums import update_post_checksum
    from misago.threads.create import create_thread
    from misago.threads.models import Post
    from misago.users.models import User

    category_id = item.source.category_id or get_category_id()
    category = Category.objects.get(pk=category_id)
    poster = User.objects.get(pk=get_poster_id())
    markup = render_event_markup(item)
    parsing = parse(markup)

    with transaction.atomic():
        thread = create_thread(category, item.title)
        thread.starter = poster
        thread.starter_name = poster.username
        thread.starter_slug = poster.slug
        thread.last_poster = poster
        thread.last_poster_name = poster.username
        thread.last_poster_slug = poster.slug
        data = dict(thread.plugin_data or {})
        data.update(thread_plugin_data(item))
        thread.plugin_data = data
        thread.save()

        post = Post(
            category=category,
            thread=thread,
            poster=poster,
            poster_name=poster.username,
            content=parsing.markup,
            content_parsed=parsing.html,
            metadata=parsing.metadata,
            posted_at=thread.started_at,
        )
        post.save()
        if hasattr(post, "set_search_document"):
            post.set_search_document(thread, parsing.text)
        update_post_checksum(post)
        if hasattr(post, "set_search_vector"):
            post.set_search_vector()
        post.save()

        thread.set_first_post(post)
        thread.set_last_post(post)
        thread.save()

        if hasattr(category, "set_last_thread"):
            category.threads = F("threads") + 1
            category.posts = F("posts") + 1
            category.set_last_thread(thread)
            category.save()

        poster.threads = F("threads") + 1
        poster.posts = F("posts") + 1
        poster.last_posted_at = thread.started_at
        poster.save(update_fields=["threads", "posts", "last_posted_at"])

        item.thread = thread
        item.status = IngestedItem.Status.PUBLISHED
        item.error = ""
        item.save(update_fields=["thread", "status", "error", "updated_at"])

    return thread


def publish_pending_items(*, limit: int | None = None) -> dict:
    queryset = IngestedItem.objects.filter(
        status=IngestedItem.Status.PENDING
    ).select_related("source")
    if limit is not None:
        queryset = queryset[:limit]

    published = 0
    failed = 0
    for item in queryset:
        try:
            publish_item(item)
            published += 1
        except Exception as exc:
            item.status = IngestedItem.Status.FAILED
            item.error = str(exc)[:4000]
            item.save(update_fields=["status", "error", "updated_at"])
            failed += 1
    return {"published": published, "failed": failed}
