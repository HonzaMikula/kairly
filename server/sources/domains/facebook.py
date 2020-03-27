import base64
import re
from functools import partial

import requests

from sources.parser import ArticleParser, split_article_to_perex_and_content

RE_FACEBOOK_ALERNATE = re.compile(r'https://(m|www).facebook.com/([^/]+)/.*')
RE_FACEBOOK_POST = re.compile(r'https://(m|www).facebook.com/([^/]+)/posts/(\d+)/?(\?.*)?')
RE_FACEBOOK_GROUP_POST = re.compile(r'https://(m|www).facebook.com/groups/([^/]+)/permalink/(\d+)/?(\?.*)?')
RE_FACEBOOK_PHOTO = re.compile(r'https://www.facebook.com/photo.php\?fbid=(\d+).*')
RE_FACEBOOK_PHOTOS_PHOTO = re.compile(r'https://(m|www).facebook.com/([^/]+)/photos/([^/]+)/(\d+).*')

RE_EMOJI_STYLE = re.compile(r'height: 16px; width: 16px; font-size: 16px; background-image: url\("([^"]+)"\)')


def extend_facebook_link(source, guid, fb_user, keep_image, post_args, htmltree):
    post_args['source'] = source
    try:
        el = htmltree.cssselect('.userContentWrapper .clearfix img')[0]
        author_name = el.attrib['aria-label']
        icon_resp = requests.get(el.attrib['src'])
        content_type = icon_resp.headers['Content-Type']
        content = base64.b64encode(icon_resp.content).decode()
        icon = f"data:{content_type};base64,{content}"

        if fb_user is None:
            for el in htmltree.cssselect('link[rel=alternate]'):
                href = el.attrib['href']
                m = RE_FACEBOOK_ALERNATE.fullmatch(href)
                if m:
                    fb_user = m.group(2)
                    break

        author = {
            'name': author_name,
            'image': icon
        }
        if fb_user:
            author['id'] = fb_user
            author['profile_url'] = f"https://www.facebook.com/{fb_user}"

        if not keep_image:
            del post_args['attachments']['image']

        try:
            message_el = htmltree.cssselect("[data-testid=post_message]")[0]
        except IndexError:
            message_el = None

        if message_el:
            for el in htmltree.cssselect('span[style]'):
                m = RE_EMOJI_STYLE.fullmatch(el.attrib['style'])
                if m:
                    emoji_url = m.group(1)
                    el.tag = 'img'
                    el.attrib.clear()
                    el.attrib['src'] = emoji_url
                    el.attrib['width'] = '16'
                    el.attrib['height'] = '16'
                    el.attrib['alt'] = el.text
                    el.text = None
                    for child in list(el):
                        el.remove(child)

            parser = ArticleParser('*')
            fragments = parser.parse(message_el)
            fragments = parser.normalize(fragments)
            perex, content = split_article_to_perex_and_content(fragments, [300, 600])
            post_args['perex'] = perex
            post_args['content'] = content

        post_args['attachments']['author'] = author
        post_args['title'] = None
        post_args['guid'] = guid
    except IndexError as e:
        print(e)
    return post_args


class FacebookImporter:
    DOMAIN = 'facebook.com'

    def match(self, url):
        m = RE_FACEBOOK_POST.fullmatch(url)
        if m:
            fb_user = m.group(2)
            fb_post_id = m.group(3)
            source = f"https://www.facebook.com/{fb_user}/posts/{fb_post_id}"
            guid = f'fb|{fb_user}_{fb_post_id}'

            url = source + '?_fb_noscript=1'
            extend_callback = partial(extend_facebook_link, source, guid, fb_user, False)
            return (url, guid, extend_callback)

        m = RE_FACEBOOK_GROUP_POST.fullmatch(url)
        if m:
            fb_group_id = m.group(2)
            fb_post_id = m.group(3)
            source = f"https://www.facebook.com/groups/{fb_group_id}/permalink/{fb_post_id}"
            guid = f'fb|{fb_group_id}_{fb_post_id}'

            url = source + '?_fb_noscript=1'
            extend_callback = partial(extend_facebook_link, source, guid, None, False)
            return (url, guid, extend_callback)

        m = RE_FACEBOOK_PHOTO.fullmatch(url)
        if m:
            fb_photo_id = m.group(1)
            source = f"https://www.facebook.com/photo.php?fbid={fb_photo_id}"
            guid = f'fb|photo:{fb_photo_id}'

            url = source + '&_fb_noscript=1'
            extend_callback = partial(extend_facebook_link, source, guid, None, True)
            return (url, guid, extend_callback)

        m = RE_FACEBOOK_PHOTOS_PHOTO.fullmatch(url)
        if m:
            fb_user = m.group(2)
            fb_album_id = m.group(3)
            fb_post_id = m.group(4)
            source = f"https://www.facebook.com/{fb_user}/photos/{fb_album_id}/{fb_post_id}"
            guid = f'fb|photo:{fb_album_id}/{fb_post_id}'

            url = source + '?_fb_noscript=1'
            extend_callback = partial(extend_facebook_link, source, guid, fb_user, True)
            return (url, guid, extend_callback)
