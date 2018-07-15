import re
import time
import traceback
import dateutil.parser

from django.core.management.base import BaseCommand

from articles.models import Post
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

    def import_post(self, channel, entry, options):
        verbosity = options.get('verbosity')

        url = entry.link.split('#', maxsplit=1)[0]

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

        if post and not options.get('force'):
            if verbosity > 1:
                self.stdout.write('Skipping {}. Already imported'.format(url))
            return post

        if verbosity > 0:
            self.stdout.write('Importing {}'.format(url))

        perex, content = channel.parse_entry(entry)

        try:
            published = entry.published
        except AttributeError:
            published = entry.date

        args = dict(
            kind=Post.NEWSPAPER,
            published=dateutil.parser.parse(published),
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
        else:
            post.__dict__.update(args)
            post.save()

        return post

    def handle(self, *args, **options):
        verbosity = options.get('verbosity')
        channels = Channel.objects.filter(enabled=True).exclude(author__isnull=True)
        if options.get('provider'):
            channels = channels.filter(provider=options['provider'])

        for channel in channels:
            if verbosity > 0:
                self.stdout.write('Fetching {}'.format(channel.rss))

            for entry in channel.parse_rss().entries:
                if not channel.is_url_valid(entry.link):
                    continue

                try:
                    post = self.import_post(channel, entry, options)

                    if channel.topic and not post.topics.filter(id=channel.topic_id).exists():
                        if verbosity > 1:
                            self.stdout.write('Assigning topic {} to {}'.format(channel.topic.name, post.guid))
                        post.topics.add(channel.topic)
                except Exception:
                    traceback.print_exc()

                time.sleep(0.05)
