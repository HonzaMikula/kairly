from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.conf import settings
from django.db import connection

from articles.models import Post


class Command(BaseCommand):
    help = 'Shift dates to make recent post released today'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            dest='dry-run',
            help='do not create anything',
        )

    def handle(self, *args, **options):
        # verbosity = options.get('verbosity')
        dry_run = options.get('dry-run', False)
        today = date.today()
        latest = None
        for d in Post.objects.filter(draft=False, source__isnull=False).order_by('-id').values_list('published', flat=True)[:20]:
            d = d.date()
            if d <= today:
                if latest is None or d > latest:
                    latest = d

        try:
            post_latest_id = Post.objects.order_by('-id').values_list('id', flat=True)[1000]
        except IndexError:
            post_latest_id = 0

        if latest is None:
            self.stdout.write('Nothing found.')
            return

        diff = (today - d).days
        if diff <= 0:
            self.stdout.write('Nothing to shift. Latest posts was published today.')
            return

        self.stdout.write(f'Latest posts are {diff} days old.')

        if not settings.DEBUG:
            self.stdout.write(f'Running command in production environment is not allowed. Exiting without shift.')

        if dry_run:
            return

        # shift only recent post, because whole databse is huge
        boundary = latest - timedelta(days=7)

        # TODO limit post by id > something, because current query is still slow
        with connection.cursor() as cursor:
            self.stdout.write(f'Shifting newspapeper subscriptions...')
            cursor.execute(f'UPDATE articles_subscription SET valid_from = valid_from + INTERVAL {diff} DAY, valid_to = valid_to + INTERVAL {diff} DAY')
            self.stdout.write(f'Shifting author subscriptions...')
            cursor.execute(f'UPDATE articles_subscriptiontoauthor SET valid_from = valid_from + INTERVAL {diff} DAY, valid_to = valid_to + INTERVAL {diff} DAY')
            self.stdout.write(f'Shifting newspaper issues...')
            cursor.execute(f'UPDATE articles_issue SET published = published + INTERVAL {diff} DAY WHERE published >= {boundary}')
            self.stdout.write(f'Shifting posts...')
            cursor.execute(f'UPDATE articles_post SET published = published + INTERVAL {diff} DAY WHERE id > {post_latest_id} AND source IS NOT NULL AND NOT draft AND published >= {boundary}')

        cache.clear()
