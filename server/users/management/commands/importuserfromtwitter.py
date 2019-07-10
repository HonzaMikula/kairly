import requests

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from users.models import User
from sources.twitter_api import get_api_connection


class Command(BaseCommand):
    help = 'Import tweets'

    def add_arguments(self, parser):
        parser.add_argument('twitter_account', nargs=1, type=str, help='Twitter account')

        parser.add_argument(
            '--username',
            action='store',
            dest='username',
            help='Local username',
        )

    def handle(self, *args, **options):
        self.api = get_api_connection()

        account = options['twitter_account'][0]
        username = options.get('username') or account.lower()  # get returns None if arg not exists

        if User.objects.filter(username=username).exists():
            raise ValueError(f"Local user with username {username} alredy exists")

        user = self.api.GetUser(screen_name=account)
        image_url = user.profile_image_url_https.replace('normal.jpg', '400x400.jpg').replace('normal.jpeg', '400x400.jpeg')

        user = User.objects.create_user(
            username=username,
            twitter_account=account,
            name=user.name,
            is_active=False,
            kind=User.PERSONAL,
            bio=user.description,
            timezone='Europe/Prague'
        )

        image_resp = requests.get(image_url)
        if image_resp.ok:
            cf = ContentFile(image_resp.content)
            user.picture.save(f"{username}.{image_url.split('.')[-1]}", cf)
            user.save()

        self.stdout.write(f"{username} created - https://kairly.com/admin/users/user/{user.id}/change/")
