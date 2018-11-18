import re
import time
import traceback
from datetime import timedelta

import dateutil.parser
from django.utils import timezone
from django.core.management.base import BaseCommand

from articles.models import Post, Newspaper, Backlog
from sources.models import Channel


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
            return None, False

        if verbosity > 0:
            self.stdout.write('Importing {}'.format(url))

        perex, content = channel.parse_entry(entry, nocache=force)

        for attr in ['published', 'date']:
            try:
                published = dateutil.parser.parse(getattr(entry, attr))
                break
            except AttributeError:
                pass
        else:
            # some fields has no published time in feed, eg kitchenette
            published = timezone.now()

        args = dict(
            kind=Post.NEWSPAPER,
            published=published,
            draft=options.get('draft'),
            guid=guid,
            source=url,
            title=entry.title,
            perex=perex,
            content=content,
            author=channel.author
        )

        if post is None:
            post = Post.objects.create(**args)
            updated = False
        else:
            post.__dict__.update(args)
            post.save()
            updated = True

        return post, updated

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
                if not channel.is_url_valid(entry.link):
                    continue

                try:
                    post, force_updated = self.import_post(channel, entry, options)

                    if post is None:
                        continue

                    counter_posts += 1

                    if force_updated:
                        continue

                    if newspaper:
                        if verbosity > 1:
                            self.stdout.write('Publishing {} in {}'.format(post.guid, channel.newspaper))

                        Backlog.objects.create(
                            newspaper=newspaper,
                            post=post,
                            publish_stamp=timezone.now(),
                        )
                except Exception:
                    self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: exception occured while fetching {}".format(timezone.now(), channel.rss))
                    traceback.print_exc()

                if options.get('last'):
                    break

                time.sleep(0.03)

        counter_end = time.perf_counter()
        self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: importtrss finished in {} / {} channels / {} posts imported".format(
            timezone.now(), timedelta(seconds=counter_end - counter_start), counter_channels, counter_posts))
