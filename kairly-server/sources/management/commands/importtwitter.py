import time
import traceback
import dateutil.parser

import twitter

from django.core.management.base import BaseCommand
from django.conf import settings

from articles.models import Post
from users.models import User


class Command(BaseCommand):
    help = 'Import tweets'

    def add_arguments(self, parser):
        parser.add_argument(
            '--account',
            action='store',
            dest='account',
            help='Import just selected twitter account',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            dest='force',
            help='Override existing posts',
        )

    def handle(self, *args, **options):
        verbosity = options.get('verbosity')

        api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
                          consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                          access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
                          access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
                          tweet_mode='extended')

        if options.get('account'):
            users = User.objects.filter(twitter_account=options['account'])
        else:
            users = User.objects.filter(twitter_account__isnull=False)

        for user in users:
            twitter_account = user.twitter_account
            try:
                if verbosity > 0:
                    self.stdout.write('Fetching @{}'.format(twitter_account))
                timeline = api.GetUserTimeline(
                    screen_name=twitter_account,
                    # exclude_replies=True, # we still want reply to account
                    trim_user=True
                )

                for status in timeline:
                    guid = 'twitter|' + status.id_str

                    # ignore retweets and replies
                    if status.retweeted_status or status.in_reply_to_status_id:
                        continue

                    source = "https://twitter.com/{}/status/{}".format(twitter_account, status.id_str)

                    try:
                        post = Post.objects.get(guid=guid)
                    except Post.DoesNotExist:
                        post = None

                    if post and not options.get('force'):
                        if verbosity > 1:
                            self.stdout.write('Skipping {}. Already imported'.format(source))
                        continue

                    title = "{}: {}...".format(twitter_account, status.full_text[:60])
                    content = status.full_text
                    for u in status.urls:
                        content = content.replace(u.url, '<a href="{}">{}</a>'.format(u.expanded_url, u.url))

                    args = dict(
                        kind=Post.TWEET,
                        published=dateutil.parser.parse(status.created_at),
                        draft=False,
                        guid=guid,
                        source=source,
                        title=title,
                        content=content,
                        author=user
                    )

                    if post is None:
                        post = Post.objects.create(**args)
                    else:
                        post.__dict__.update(args)
                        post.save()

                    # # Topics are not supported for now
                    # if channel.topic:
                    #     if verbosity > 1:
                    #         self.stdout.write('Assigning topic {} to {}'.format(channel.topic.name, post.guid))
                    #     post.topics.add(channel.topic)

            except Exception:
                traceback.print_exc()

            time.sleep(0.05)
