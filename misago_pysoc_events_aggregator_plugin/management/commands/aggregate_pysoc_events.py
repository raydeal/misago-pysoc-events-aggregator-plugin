from django.core.management.base import BaseCommand

from ...ingest.pipeline import ingest_source
from ...models import Source
from ...publish.threads import publish_pending_items


class Command(BaseCommand):
    help = "Fetch configured RSS/HTML event sources and publish new Misago threads."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Ignore poll intervals and fetch every enabled source.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Fetch and parse sources without writing items or threads.",
        )
        parser.add_argument(
            "--no-publish",
            action="store_true",
            help="Ingest new items without creating forum threads.",
        )

    def handle(self, *args, **options):
        force = options["force"]
        dry_run = options["dry_run"]
        created_total = 0
        events_total = 0

        for source in Source.objects.filter(enabled=True).order_by("name"):
            try:
                result = ingest_source(source, force=force, dry_run=dry_run)
            except Exception as exc:
                source.last_error = str(exc)[:4000]
                source.save(update_fields=["last_error", "updated_at"])
                self.stderr.write(
                    self.style.ERROR(f"{source.name}: {exc}")
                )
                continue

            if result.get("skipped"):
                self.stdout.write(f"{source.name}: skipped (poll interval)")
                continue

            created_total += result["created"]
            events_total += result["events"]
            self.stdout.write(
                f"{source.name}: {result['events']} events, "
                f"{result['created']} new, {result['seen']} already known"
            )

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run: nothing was published."))
            return

        if options["no_publish"]:
            self.stdout.write("Ingest finished; publishing skipped.")
            return

        publish_result = publish_pending_items()
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. {created_total} new items from {events_total} events; "
                f"{publish_result['published']} threads created, "
                f"{publish_result['failed']} failed."
            )
        )
