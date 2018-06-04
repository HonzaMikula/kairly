import time
import traceback
import dateutil.parser

import twitter

from django.core.management.base import BaseCommand
from django.conf import settings

from articles.models import Post
from sources.models import TwitterChannel


class Command(BaseCommand):
    help = 'Import tweets'

    def add_arguments(self, parser):
        parser.add_argument(
            '--account',
            action='store',
            dest='account',
            help='Import just selected twitter account',
        )

    def handle(self, *args, **options):
        verbosity = options.get('verbosity')

        api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
                          consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                          access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
                          access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)

        channels = TwitterChannel.objects.filter(enabled=True).exclude(author__isnull=True)
        if options.get('account'):
            channels = channels.filter(twitter_account=options['account'])

        for channel in channels:
            try:
                if verbosity > 0:
                    self.stdout.write('Fetching @{}'.format(channel.twtter_account))
                timeline = api.GetUserTimeline(screen_name=channel.twtter_account)

                for status in timeline:
                    guid = 'twitter|' + status.id_str

                    if Post.objects.filter(guid=guid).exists():
                        continue

                    title = "{}: {}...".format(channel.twtter_account, status.text[:60])
                    args = dict(
                        kind=Post.TWEET,
                        published=dateutil.parser.parse(status.created_at),
                        draft=False,
                        guid=guid,
                        title=title,
                        content=status.text,
                        author=channel.author
                    )

                    post = Post.objects.create(**args)
                    if channel.topic:
                        if verbosity > 1:
                            self.stdout.write('Assigning topic {} to {}'.format(channel.topic.name, post.guid))
                        post.topics.add(channel.topic)

            except Exception:
                traceback.print_exc()

            time.sleep(0.05)
