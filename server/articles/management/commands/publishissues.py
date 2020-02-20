import traceback
import datetime
from datetime import timedelta
import time

import pytz

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from django.db.models import Max
from django.utils.timezone import now as timezone_now

from articles.models import Newspaper, Issue, Backlog, BacklogPost, IssuePost, Editorial, EditorialTweet, Post
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
            '--newspaper',
            action='store',
            dest='newspaper',
            help='Newspaper only',
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

        backlog = Backlog.objects.get(newspaper=newspaper, name='upcoming')
        if (backlog.layout == '[]'):
            return

        if verbosity > 0:
            self.stdout.write('Creating {} #{}'.format(newspaper, number))

        issue = Issue(
            number=number,
            published=now,
            editor=newspaper.editor,
            newspaper=newspaper,
            layout=backlog.layout
        )

        if not dry_run:
            issue.save()

        refs = []
        post_ids = []
        for bp in BacklogPost.objects.filter(backlog=backlog):
            if verbosity > 0:
                self.stdout.write('Adding post {}'.format(bp.post))

            refs.append(IssuePost(issue=issue, post_id=bp.post_id))
            post_ids.append(bp.post_id)

        if not dry_run:
            IssuePost.objects.bulk_create(refs)
            Post.objects.filter(id__in=post_ids, kind=Post.COMMENT).update(draft=False, published=timezone_now())
            backlog.delete()
            Backlog.objects.filter(newspaper=newspaper, name='next').update(name='upcoming')

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

        newspaper_name = options.get('newspaper')
        if newspaper_name is not None:
            username, newspaper_slug = newspaper_name.split('/')
            query = Newspaper.objects.filter(editor__username=username, slug=newspaper_slug)
        else:
            query = Newspaper.objects.all()

        query = query\
            .filter(backlog__name='upcoming')\
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
