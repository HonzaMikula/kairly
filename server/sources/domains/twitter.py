import re
import orjson as json

from articles.models import Post
from sources.twitter_api import get_api_connection, status_to_post_args


RE_TWITTER_URL = re.compile(r'https://(mobile\.)?twitter\.com/[^/]+/status/(\d+)(\?.*)?')


def create_twitter_link(status_id):
    try:
        return Post.objects.get(guid=f'twitter|{status_id}', kind=Post.TWEET)
    except Post.DoesNotExist:
        api = get_api_connection()
        status = api.GetStatus(status_id)
        args = status_to_post_args(api, status, dump_attachments=False)
        attachments = args['attachments'] or []
        attachments.append({
            'type': 'author',
            'id': status.user.id,
            'name': status.user.name,
            'screen_name': status.user.screen_name,
            'profile_image_url_https': status.user.profile_image_url_https,
        })
        args['attachments'] = json.dumps(attachments).decode()
        return Post.objects.create(**args)


class TwitterImporter:
    DOMAIN = 'twitter.com'

    def match(self, url):
        m = RE_TWITTER_URL.fullmatch(url)
        if m:
            return create_twitter_link(m.group(2))
