import re
import rapidjson as json
from urllib.parse import urlsplit

import bs4
import twitter
import requests
import dateutil.parser
from django.conf import settings

from articles.models import Post


def get_api_connection():
    return twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
                       consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                       access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
                       access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
                       tweet_mode='extended')


def _get_attachements(api, status):
    content = status.full_text

    external_urls = []
    already_added_urls = set()
    media = []
    quoted_status_item = []

    for u in status.urls:
        quoted_status_id_str = getattr(status, 'quoted_status_id_str')
        if quoted_status_id_str and u.expanded_url.endswith(quoted_status_id_str):
            if status.quoted_status:
                user = api.GetUser(user_id=status.quoted_status.user.id_str)
                user_url = 'https://twitter.com/' + user.screen_name
                quoted_content, quoted_attachments = _get_attachements(api, status.quoted_status)
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
                content_type = resp.headers.get('Content-Type')
                if content_type in ['text/html', 'application/xhtml+xml']:
                    page_title = bs4.BeautifulSoup(resp.content, "lxml").title.text
                else:
                    page_title = resp.url[:25]
                    if page_title != resp.url:
                        page_title += '…'

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

                if attachment['href'] in already_added_urls:
                    continue

                external_urls.append(attachment)
                already_added_urls.add(attachment['href'])
            except IOError:
                page_title = u.expanded_url

            link_body = pu.netloc + pu.path
            if len(link_body) > 30:
                link_body = link_body[:30].rstrip('.') + '…'
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


def get_post_guid(status):
    return 'twitter|' + status.id_str


def status_to_post_args(api, status, *, screen_name=None, dump_attachments=True):
    screen_name = screen_name or status.user.screen_name
    title = "{}: {}...".format(screen_name, status.full_text[:60].replace('\n', ' '))
    content, attachments = _get_attachements(api, status)

    source = "https://twitter.com/{}/status/{}".format(screen_name, status.id_str)

    if dump_attachments:
        attachments = json.dumps(attachments) if attachments else None

    return dict(
        kind=Post.TWEET,
        published=dateutil.parser.parse(status.created_at),
        draft=False,
        guid=get_post_guid(status),
        source=source,
        title=title,
        content=content,
        attachments=attachments,
    )
