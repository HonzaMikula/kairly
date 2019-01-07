import rapidjson as json
import re
import time
import traceback
import dateutil.parser
from urllib.parse import urlsplit
from datetime import timedelta

import twitter
import requests
import bs4

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

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

    def get_attachements(self, status):
        content = status.full_text

        external_urls = []
        media = []
        quoted_status_item = []

        for u in status.urls:
            quoted_status_id_str = getattr(status, 'quoted_status_id_str')
            if quoted_status_id_str and u.expanded_url.endswith(quoted_status_id_str):
                if status.quoted_status:
                    user = self.api.GetUser(user_id=status.quoted_status.user.id_str)
                    user_url = 'https://twitter.com/' + user.screen_name
                    quoted_content, quoted_attachments = self.get_attachements(status.quoted_status)
                    quoted_status_item = {
                        'type': 'quoted_status',
                        'id': quoted_status_id_str,
                        'user': {
                            'name': user.name,
                            'screen_name': user.screen_name,
                            'url': user_url,
                        },
                        'content': quoted_content,
                        'attachments': quoted_attachments,
                    }
                    content = content.replace(u.url, '')
                else:
                    quoted_status_item = {
                        'type': 'quoted_status.unavailable'
                    }
                    content = content.replace(u.url, '<a href="{}">{}</a>'.format(u.url, u.url))
            else:
                pu = urlsplit(u.expanded_url)

                try:
                    resp = requests.get(u.expanded_url, timeout=10)
                    page_title = bs4.BeautifulSoup(resp.content, "lxml").title.text
                    parsed_url = urlsplit(resp.url)  # take final url adter redirects
                    attachment = {
                        'type': 'url',
                        'title': page_title,
                        'host': parsed_url.netloc
                    }

                    local_post = Post.find_by_source_url(resp.url)
                    if local_post:
                        attachment['source_href'] = resp.url
                        attachment['href'] = '/{}/{}'.format(
                            local_post.author.username, local_post.slug)
                        attachment['title'] = local_post.title
                    else:
                        attachment['href'] = resp.url
                        attachment['title'] = page_title

                    external_urls.append(attachment)
                except IOError:
                    page_title = u.expanded_url

                link_body = pu.netloc + pu.path
                if len(link_body) > 30:
                    link_body = link_body[:30] + '…'
                content = content.replace(u.url, '<a href="{}" title="{}">{}</a>'.format(u.expanded_url, page_title, link_body))

        for m in (status.media or []):
            item = {
                'type': 'media.' + m.type,
                'id': m.id,
                'src': m.media_url_https,
                'sizes': m.sizes,
            }
            if m.video_info:
                item['video_info'] = m.video_info

            media.append(item)
            content = content.replace(m.url, '')

        for u in status.user_mentions:
            pattern = re.compile('(@' + re.escape(u.screen_name) + ')', re.IGNORECASE)
            content = pattern.sub('<a href="https://twitter.com/{}" title="{}">\\1</a>'.format(u.screen_name, u.name), content)
            # content = content.replace('@' + u.screen_name, )

        attachments = external_urls + media
        if quoted_status_item:
            attachments.append(quoted_status_item)

        return content, attachments or None

    def handle(self, *args, **options):
        verbosity = options.get('verbosity')

        counter_start = time.perf_counter()
        counter_accounts = 0
        counter_tweets = 0
        self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: importtwitter started".format(timezone.now()))

        self.api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
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
                    guid = 'twitter|' + status.id_str

                    # ignore retweets and replies
                    if status.retweeted_status or status.in_reply_to_status_id:
                        continue

                    # print("-----------------------------")
                    # print(json.dumps(status.AsDict(), indent=2, ensure_ascii=False))

                    source = "https://twitter.com/{}/status/{}".format(twitter_account, status.id_str)

                    try:
                        post = Post.objects.get(guid=guid)
                    except Post.DoesNotExist:
                        post = None

                    if post and not options.get('force'):
                        if verbosity > 1:
                            self.stdout.write('Skipping {}. Already imported'.format(source))
                        continue

                    title = "{}: {}...".format(twitter_account, status.full_text[:60].replace('\n', ' '))
                    content, attachments = self.get_attachements(status)

                    args = dict(
                        kind=Post.TWEET,
                        published=dateutil.parser.parse(status.created_at),
                        draft=False,
                        guid=guid,
                        source=source,
                        title=title,
                        content=content,
                        attachments=json.dumps(attachments) if attachments else None,
                        author=user
                    )

                    if post is None:
                        post = Post.objects.create(**args)
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
