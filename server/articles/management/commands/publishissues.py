import traceback
import datetime
from datetime import timedelta
import time

import pytz

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from django.db.models import Max

from articles.models import Newspaper, Issue, Backlog, IssuePost, Editorial, EditorialTweet
from articles.period import PeriodMixin


class Command(BaseCommand):
    help = 'Release issues with posts marked to publish'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hour',
            action='store',
            dest='hour',
            help='Fake time for which time issues should be published. Use H+TZ form, eg 9+02 for 9:00 in Europe/Prague zone',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            dest='dry-run',
            help='do not create anything',
        )

    @transaction.atomic
    def create_issue(self, newspaper, now, verbosity, dry_run):
        mx_num = Issue.objects.filter(newspaper=newspaper)\
            .aggregate(Max('number'))['number__max']
        number = 1 if mx_num is None else mx_num + 1

        if verbosity > 0:
            self.stdout.write('Creating {} #{}'.format(newspaper, number))

        backlog_items = list(
            Backlog.objects
            .filter(newspaper=newspaper, publish_in=Backlog.UPCOMING_ISSUE)
            .order_by('ordering', 'post__published')
            .select_related('post'))

        if backlog_items:
            if not dry_run:
                issue = Issue.objects.create(
                    number=number,
                    published=now,
                    editor=newspaper.editor,
                    newspaper=newspaper
                )

            for i, backlog in enumerate(backlog_items):
                if verbosity > 0:
                    self.stdout.write('Adding post {}'.format(backlog.post))
                if not dry_run:
                    backlog.delete()

                    editorial = backlog.editorial
                    if editorial and editorial.kind == Editorial.TWEETS and EditorialTweet.objects.filter(editorial=editorial).count() == 0:
                        # ignore editorial with no tweets
                        editorial.delete()
                        editorial = None

                    IssuePost.objects.create(
                        issue=issue, post=backlog.post, editorial=editorial, ordering=i)

        Backlog.objects.filter(newspaper=newspaper, publish_in=Backlog.NEXT_ISSUE).update(publish_in=Backlog.UPCOMING_ISSUE)

    def get_now(self, hour=None):
        now = timezone.now().replace(minute=0, second=0, microsecond=0)

        if hour is not None:
            default_tz = timezone.get_default_timezone()
            h, *tail = map(int, hour.split('+', maxsplit=1))
            if tail:
                tz = datetime.timezone(timedelta(hours=tail[0]))
            else:
                tz = default_tz

            now = now.astimezone(tz).replace(hour=h).astimezone(default_tz)

        return now

    def handle(self, *args, **options):
        verbosity = options.get('verbosity')
        dry_run = options.get('dry-run', False)

        counter_start = time.perf_counter()
        counter_issues = 0
        self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: publishissues started".format(timezone.now()))

        now = self.get_now(options.get('hour'))
        if verbosity > 1:
            self.stdout.write('Serching for issues to be published at {}'.format(now))

        query = Newspaper.objects\
            .filter(backlog__publish_in__isnull=False)\
            .select_related('editor')\
            .distinct()

        for newspaper in query:
            try:
                editor_tz = pytz.timezone(newspaper.editor.timezone)
                now = now.astimezone(editor_tz)

                if newspaper.period == PeriodMixin.X6_PER_DAY:
                    if now.hour not in PeriodMixin.X6_PER_DAY_HOURS:
                        continue
                elif newspaper.period == PeriodMixin.X3_PER_DAY:
                    if now.hour not in PeriodMixin.X3_PER_DAY_HOURS:
                        continue
                else:
                    if now.hour != newspaper.period_time.hour:
                        continue

                    if newspaper.period == PeriodMixin.WEEKLY:
                        if now.isoweekday() != newspaper.period_dow:
                            continue

                self.create_issue(newspaper, now, verbosity, dry_run)
                counter_issues += 1
            except Exception:
                self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: exception occured while handling {}".format(timezone.now(), newspaper))
                traceback.print_exc()

        counter_end = time.perf_counter()
        self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: publishissues finished in {} / {} issues published".format(
            timezone.now(), timedelta(seconds=counter_end - counter_start), counter_issues))
