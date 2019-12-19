import hashlib
import re
import time
import traceback
import lxml.html
from datetime import timedelta

import dateutil.parser
from django.utils import timezone
from django.core.management.base import BaseCommand

from articles.models import Post, Newspaper, Backlog, IssuePost
from articles.signals import post_publish
from articles.utils import create_post_link
from sources.models import Channel, EntryHasNoContentException
from articles.models import SubscriptionToAuthor
from users.models import User


# additional timezones which are not recognized byt dateutil.parser by default
TZ_INFOS = {
    'PST': dateutil.tz.gettz('US/Pacific'),
    'PDT': dateutil.tz.gettz('US/Pacific'),
    'PT': dateutil.tz.gettz('US/Pacific'),
    'MST': dateutil.tz.gettz('US/Mountain'),
    'MDT': dateutil.tz.gettz('US/Mountain'),
    'MT': dateutil.tz.gettz('US/Mountain'),
    'CST': dateutil.tz.gettz('US/Central'),
    'CDT': dateutil.tz.gettz('US/Central'),
    'CT': dateutil.tz.gettz('US/Central'),
    'EST': dateutil.tz.gettz('US/Eastern'),
    'EDT': dateutil.tz.gettz('US/Eastern'),
    'ET': dateutil.tz.gettz('US/Eastern')
}


class Command(BaseCommand):
    help = 'Import posts from RSS channels'

    def add_arguments(self, parser):
        parser.add_argument(
            '--provider',
            action='store',
            dest='provider',
            help='Import just selected provider',
        )
        parser.add_argument(
            '--subscriptions-of',
            action='store',
            dest='subscriptions-of',
            help='Import just providers subscribed by given user',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            dest='force',
            help='Override existing posts',
        )
        parser.add_argument(
            '--nosleep',
            action='store_true',
            dest='nosleep',
            help='Do not wait between requests',
        )
        parser.add_argument(
            '--draft',
            action='store_true',
            dest='draft',
            help='Create posts as draft',
        )
        parser.add_argument(
            '--url',
            action='store',
            dest='url',
            help='Import only post with selected url (debug option)',
        )

    def handle(self, *args, **options):
        verbosity = options.get('verbosity')

        counter_start = time.perf_counter()
        counter_channels = 0
        counter_posts = 0
        self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: importrss started".format(timezone.now()))

        channels = Channel.objects.filter(enabled=True).exclude(author__isnull=True)
        if options.get('provider'):
            channels = channels.filter(provider=options['provider'])
        elif options.get('subscriptions-of'):
            user = User.objects.get(username=options['subscriptions-of'])
            authors = []
            for subscription in SubscriptionToAuthor.objects.filter(user=user).select_related('author'):
                authors.append(subscription.author_id)
            channels = channels.filter(author_id__in=authors)

        for channel in channels:
            if verbosity > 0:
                self.stdout.write('Fetching {}'.format(channel.rss))

            counter_channels += 1

            newspaper = None
            if channel.newspaper:
                username, slug = channel.newspaper.split('/')
                newspaper = Newspaper.objects.get(slug=slug, editor__username=username)

            for entry in channel.parse_rss().entries:
                try:
                    post, imported = _import_feed_entry(
                        channel, entry, self.stdout,
                        verbosity=options.get('verbosity'),
                        force=options.get('force'),
                        only_url=options.get('url'),
                        draft=options.get('draft'),
                    )

                    if post is None:
                        continue

                    if imported:
                        counter_posts += 1

                    if newspaper and post.kind not in [Post.RECOMMENDATION, Post.LINK]:
                        if IssuePost.objects.filter(issue__newspaper=newspaper, post=post).exists():
                            continue
                        if Backlog.objects.filter(newspaper=newspaper, post=post).exists():
                            continue

                        if verbosity > 1:
                            self.stdout.write('Publishing {} in {}'.format(post.guid, channel.newspaper))

                        Backlog.objects.create(
                            newspaper=newspaper,
                            post=post,
                            publish_in=Backlog.UPCOMING_ISSUE,
                        )
                except Exception:
                    self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: exception occured while fetching {} from feed {}".format(timezone.now(), getattr(entry, 'link', ''), channel.rss))
                    traceback.print_exc()

                if not options.get('nosleep'):
                    time.sleep(0.01)

        counter_end = time.perf_counter()
        self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: importtrss finished in {} / {} channels / {} posts imported".format(
            timezone.now(), timedelta(seconds=counter_end - counter_start), counter_channels, counter_posts))


def import_feed_entry(channel, entry):
    post, _ = _import_feed_entry(channel, entry, verbosity=3)
    return post


def get_entry_publish_date(entry):
    for attr in ['published', 'date']:
        try:
            return dateutil.parser.parse(getattr(entry, attr), tzinfos=TZ_INFOS)
        except AttributeError:
            pass

    # some fields has no published time in feed, eg kitchenette
    return timezone.now()


def _import_feed_entry(channel, entry, stdout=None, verbosity=0, force=False, only_url=None, draft=False):
    if not hasattr(entry, 'link'):
        stdout and stdout.write("Entry {} is missing link attribute".format(entry))
        return None, None

    if not channel.is_url_valid(entry.link):
        return None, None

    try:
        return _import_post(channel, entry, stdout, verbosity, force, only_url, draft)
    except EntryHasNoContentException:
        stdout and stdout.write("Entry {} is missing content/description attribute".format(entry))


def _get_title_from_entry(entry):
    detail = entry.title_detail
    if detail['type'] == 'text/html':
        return lxml.html.fromstring(detail['value']).text_content()
    return detail['value']


def _import_post(channel, entry, stdout, verbosity, force, only_url, draft):
    url = entry.link.split('#', maxsplit=1)[0]

    if only_url and url != only_url:
        return None, False

    # some feeds has not guid attribute
    if hasattr(entry, 'id'):
        entry_id = entry.id
    elif url:
        entry_id = re.sub('^https?://', '', url)
    else:
        h = hashlib.sha1()
        h.update(entry.description.encode('utf-8'))
        h.update(entry.published.encode('utf-8'))
        entry_id = h.hexdigest()
    guid = "{}|{}".format(channel.provider, entry_id)[:255]  # trim to field's max length

    try:
        post = Post.objects.get(guid=guid)
    except Post.DoesNotExist:
        post = None

    if post and not force:
        if verbosity > 1:
            stdout and stdout.write('Skipping {}. Already imported'.format(url))
        return post, False

    if verbosity > 0:
        stdout and stdout.write('Importing {}'.format(url))

    published = get_entry_publish_date(entry)

    if channel.import_links:
        post = create_post_link(url, channel.author, hidden=False, published=published, guid=guid)
        if post.kind == Post.LINK:
            return post, True

        # post already exists under regular author, add recommendation instead
        recommendation = Post.objects.create(
            title=post.title,
            kind=Post.RECOMMENDATION,
            author=channel.author,
            guid=guid,
            ref_post=post,
            protected=False,
            published=published,
        )
        return recommendation, True

    args = channel.parse_entry(entry, usecache=False)

    title_directives = channel.get_directives('replace', 'title')
    title = _get_title_from_entry(entry)
    for directive in title_directives:
        title = directive.replace(title)

    args.update(dict(
        published=published,
        draft=draft,
        guid=guid,
        title=title,
        author=channel.author,
    ))

    if post is None:
        post = Post.objects.create(**args)
        post_publish.send(sender=Command, post=post)
    else:
        post.__dict__.update(args)
        post.save()

    return post, True
