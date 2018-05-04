import time
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

    def handle(self, *args, **options):
        channels = Channel.objects.filter(enabled=True).exclude(author__isnull=True)
        if options.get('provider'):
            channels = channels.filter(provider=options['provider'])

        for channel in channels:
            self.stdout.write('Fetching {}'.format(channel.rss))

            for entry in channel.parse_rss().entries:
                guid = "{}|{}".format(channel.provider, entry.id)

                if not channel.is_url_valid(entry.link):
                    continue

                url = entry.link.split('#', maxsplit=1)[0]
                perex, content = channel.parse_entry(entry)
                update = False

                if Post.objects.filter(guid=guid).exists():
                    if options.get('force'):
                        update = True
                    else:
                        self.stdout.write('Skipping {}. Already imported'.format(url))
                        continue

                args = dict(
                    kind=Post.NEWSPAPER,
                    published=dateutil.parser.parse(entry.published),
                    draft=options.get('draft'),
                    guid=guid,
                    source=url,
                    title=entry.title,
                    perex=perex,
                    content=content,
                    author=channel.author
                )

                if update:
                    post = Post.objects.get(guid=guid)
                    post.__dict__.update(args)
                    post.save()
                else:
                    Post.objects.create(**args)

                self.stdout.write('Imported {}'.format(url))
                time.sleep(0.1)
