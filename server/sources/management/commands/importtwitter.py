import time
import traceback
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from articles.models import Post
from articles.signals import post_publish
from users.models import User
from sources.twitter_api import get_api_connection, get_post_guid, status_to_post_args


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

        counter_start = time.perf_counter()
        counter_accounts = 0
        counter_tweets = 0
        self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: importtwitter started".format(timezone.now()))

        self.api = get_api_connection()

        if options.get('account'):
            users = User.objects.filter(twitter_account=options['account'])
        else:
            users = User.objects.filter(twitter_account__isnull=False)

        for user in users:
            twitter_account = user.twitter_account
            try:
                if verbosity > 0:
                    self.stdout.write('Fetching @{}'.format(twitter_account))
                timeline = self.api.GetUserTimeline(
                    screen_name=twitter_account,
                    # exclude_replies=True, # we still want reply to account
                    trim_user=True
                )

                # import pickle
                # import rapidjson as json
                # # with open('/mnt/c/Users/farin/w/etabery.pickle', 'wb') as f:
                # #     pickle.dump(timeline, f)
                # with open('/mnt/c/Users/farin/w/jiripehe.pickle', 'rb') as f:
                #     timeline = reversed(pickle.load(f))

                for status in timeline:
                    guid = get_post_guid(status)

                    # ignore retweets and replies
                    if status.retweeted_status or status.in_reply_to_status_id:
                        continue

                    # print("-----------------------------")
                    # print(json.dumps(status.AsDict(), indent=2, ensure_ascii=False))

                    try:
                        post = Post.objects.get(guid=guid)
                    except Post.DoesNotExist:
                        post = None

                    if post and not options.get('force'):
                        if verbosity > 1:
                            self.stdout.write('Skipping {}. Already imported'.format(guid))
                        continue

                    args = status_to_post_args(self.api, status)
                    args['author'] = user

                    if post is None:
                        post = Post.objects.create(**args)
                        post_publish.send(sender=self.__class__, post=post)
                    else:
                        post.__dict__.update(args)
                        post.save()

                    counter_tweets += 1

            except Exception:
                self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: exception occured while fetching @{}".format(timezone.now(), twitter_account))
                traceback.print_exc()

            counter_accounts += 1
            time.sleep(0.03)

        counter_end = time.perf_counter()
        self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: importtwitter finished in {} / {} twitter accounts / {} tweets imported".format(
            timezone.now(), timedelta(seconds=counter_end - counter_start), counter_accounts, counter_tweets))
