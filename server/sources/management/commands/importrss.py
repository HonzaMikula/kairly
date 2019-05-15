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
            '--last',
            action='store_true',
            dest='last',
            help='Import single document only for each channel (debug option)',
        )
        parser.add_argument(
            '--url',
            action='store',
            dest='url',
            help='Import only post with selected url (debug option)',
        )

    def import_post(self, channel, entry, options):
        verbosity = options.get('verbosity')
        force = options.get('force')

        url = entry.link.split('#', maxsplit=1)[0]

        if options.get('url') and url != options.get('url'):
            return None, False

        # some feeds has not guid attribute
        if hasattr(entry, 'id'):
            entry_id = entry.id
        else:
            entry_id = re.sub('^https?://', '', url)
        guid = "{}|{}".format(channel.provider, entry_id)

        try:
            post = Post.objects.get(guid=guid)
        except Post.DoesNotExist:
            post = None

        if post and not force:
            if verbosity > 1:
                self.stdout.write('Skipping {}. Already imported'.format(url))
            return post, False

        if verbosity > 0:
            self.stdout.write('Importing {}'.format(url))

        if channel.import_links:
            post = create_post_link(url, channel.author, False, guid=guid)
            if post.kind == Post.LINK:
                return post, True

            # post already exists under regular author, add recommendation instead
            recommendation = Post.objects.create(
                title=post.title,
                kind=Post.RECOMMENDATION,
                author=channel.author,
                guid=guid,
                ref_post=post,
                protected=False
            )
            return recommendation, True

        perex, content, resolved_url = channel.parse_entry(entry, nocache=force)

        for attr in ['published', 'date']:
            try:
                published = dateutil.parser.parse(getattr(entry, attr), tzinfos=TZ_INFOS)
                break
            except AttributeError:
                pass
        else:
            # some fields has no published time in feed, eg kitchenette
            published = timezone.now()

        replacements = [d for d in channel.get_directives('replace', 'title')]
        title = self.get_title_from_entry(entry)
        for replacement in replacements:
            title = replacement.replace(title)

        replacements = [d for d in channel.get_directives('replace', 'document')]
        for replacement in replacements:
            perex = replacement.replace(perex)
            content = replacement.replace(content)

        args = dict(
            kind=Post.NEWSPAPER,
            published=published,
            draft=options.get('draft'),
            guid=guid,
            source=resolved_url,
            title=title,
            perex=perex,
            content=content,
            author=channel.author
        )

        if post is None:
            post = Post.objects.create(**args)
            post_publish.send(sender=self.__class__, post=post)
        else:
            post.__dict__.update(args)
            post.save()

        return post, True

    def get_title_from_entry(self, entry):
        detail = entry.title_detail
        if detail['type'] == 'text/html':
            return lxml.html.fromstring(detail['value']).text_content()
        return detail['value']

    def handle(self, *args, **options):
        verbosity = options.get('verbosity')

        counter_start = time.perf_counter()
        counter_channels = 0
        counter_posts = 0
        self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: importrss started".format(timezone.now()))

        channels = Channel.objects.filter(enabled=True).exclude(author__isnull=True)
        if options.get('provider'):
            channels = channels.filter(provider=options['provider'])

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
                    if not hasattr(entry, 'link'):
                        self.stdout.write("Entry {} is missing link attribute".format(entry))
                        continue

                    if not channel.is_url_valid(entry.link):
                        continue

                    try:
                        post, imported = self.import_post(channel, entry, options)
                    except EntryHasNoContentException:
                        self.stdout.write("Entry {} is missing content/description attribute".format(entry))

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
                            publish_stamp=timezone.now(),
                        )
                except Exception:
                    self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: exception occured while fetching {} from feed {}".format(timezone.now(), getattr(entry, 'link', ''), channel.rss))
                    traceback.print_exc()

                if options.get('last'):
                    break

                if not options.get('nosleep'):
                    time.sleep(0.01)

        counter_end = time.perf_counter()
        self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: importtrss finished in {} / {} channels / {} posts imported".format(
            timezone.now(), timedelta(seconds=counter_end - counter_start), counter_channels, counter_posts))
