from decimal import Decimal

from dateutil.relativedelta import relativedelta

from django.utils import timezone
from django.core.management.base import BaseCommand

from articles.models import Post
from users.models import User


class Command(BaseCommand):
    help = 'Show cost of author posts'

    def add_arguments(self, parser):
        parser.add_argument('usernames', nargs='*', type=str, help='Users to show')

        parser.add_argument(
            '--month',
            action='store',
            dest='month',
            help='Force month to assign (eg 12/2018), default current month',
        )
        parser.add_argument(
            '--include-free',
            action='store_true',
            dest='include_free',
            help='Include free articles',
        )

    def handle(self, *args, **options):
        month = options.get('month')
        t = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        if month:
            m, y = map(int, month.split('/'))
            t = t.replace(year=y, month=m)

        interval = (t, t + relativedelta(months=1))

        for username in options.get('usernames'):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write('* {} does not exist.'.format(username))
                continue

            query = Post.objects.filter(
                draft=False,
                published__gte=interval[0],
                published__lt=interval[1],
                author=user
            )
            if not options.get('include_free'):
                query = query.filter(author_price__gt=0)

            posts = list(query.order_by('published').values('title', 'weight', 'author_price'))

            total_weight = Decimal(sum(p['weight'] or 0 for p in posts))

            self.stdout.write('* {}'.format(user.username))
            for post in posts:
                if post['weight'] is None:
                    # should happen only for not fully migrated db
                    self.stdout.write('  NO WEIGHT! - {}'.format(post['title'].replace('\n', ' ')))
                    continue
                post_cost = post['author_price'] * Decimal(post['weight']) / total_weight
                post_cost = post_cost.quantize(Decimal('.01'))
                self.stdout.write('  {} - {}'.format(post_cost, post['title'].replace('\n', ' ')))
