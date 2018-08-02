import traceback
import datetime

import pytz

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from django.db.models import Max

from articles.models import Newspaper, Issue, Backlog, IssuePost
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
    def create_edition_issue(self, edition, now, verbosity, dry_run):
        mx_num = Issue.objects.filter(edition=edition)\
            .aggregate(Max('number'))['number__max']
        number = 1 if mx_num is None else mx_num + 1

        if verbosity > 0:
            self.stdout.write('Creating {} #{}'.format(edition, number))

        if not dry_run:
            issue = Issue.objects.create(
                number=number,
                published=now,
                editor=edition.editor,
                edition=edition
            )

        backlog_query = Backlog.objects\
            .filter(edition=edition, publish_stamp__isnull=False)\
            .order_by('ordering')\
            .select_related('post')

        for i, backlog in enumerate(backlog_query):
            if verbosity > 0:
                self.stdout.write('Adding post {}'.format(backlog.post))
            if not dry_run:
                IssuePost.objects.create(
                    edition=issue, post=backlog.post, ordering=i)
                backlog.delete()

    def get_now(self, hour=None):
        now = timezone.now().replace(minute=0, second=0, microsecond=0)

        if hour is not None:
            default_tz = timezone.get_default_timezone()
            h, *tail = map(int, hour.split('+', maxsplit=1))
            if tail:
                tz = datetime.timezone(datetime.timedelta(hours=tail[0]))
            else:
                tz = default_tz

            now = now.astimezone(tz).replace(hour=h).astimezone(default_tz)

        return now

    def handle(self, *args, **options):
        verbosity = options.get('verbosity')
        dry_run = options.get('dry-run', False)

        now = self.get_now(options.get('hour'))
        if verbosity > 1:
            self.stdout.write('Serching for issues to be published at {}'.format(now))

        query = Newspaper.objects\
            .filter(editionbacklog__publish_stamp__isnull=False)\
            .select_related('editor')\
            .distinct()

        for edition in query:
            try:
                editor_tz = pytz.timezone(edition.editor.timezone)
                now = now.astimezone(editor_tz)

                if edition.period == PeriodMixin.X3_PER_DAY:
                    if now.hour not in PeriodMixin.X3_PER_DAY_HOURS:
                        continue
                else:
                    if now.hour != edition.period_time.hour:
                        continue

                    if edition.period == PeriodMixin.WEEKLY:
                        if now.isoweekday() != edition.period_dow:
                            continue

                self.create_edition_issue(edition, now, verbosity, dry_run)
            except Exception:
                traceback.print_exc()
