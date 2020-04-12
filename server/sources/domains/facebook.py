import base64
import re
from functools import partial

import requests

from sources.parser import ArticleParser, split_article_to_perex_and_content

RE_FACEBOOK_ALERNATE = re.compile(r'https://(m|www).facebook.com/([^/]+)/?.*')
RE_FACEBOOK_POST = re.compile(r'https://(m|www).facebook.com/([^/]+)/posts/(\d+)/?(\?.*)?')
RE_FACEBOOK_GROUP_POST = re.compile(r'https://(m|www).facebook.com/groups/([^/]+)/permalink/(\d+)/?(\?.*)?')
RE_FACEBOOK_PHOTO = re.compile(r'https://www.facebook.com/photo.php\?fbid=(\d+).*')
RE_FACEBOOK_PHOTOS_PHOTO = re.compile(r'https://(m|www).facebook.com/([^/]+)/photos/([^/]+)/(\d+).*')
RE_FACEBOOK_NOTE = re.compile(r'https://(m|www).facebook.com/notes/([^/]+)/([^/]+)/(\d+).*')

RE_EMOJI_STYLE = re.compile(r'height: 16px; width: 16px; font-size: 16px; background-image: url\("([^"]+)"\)')


def download_icon(url):
    resp = requests.get(url)
    if resp.ok:
        content_type = resp.headers['Content-Type']
        content = base64.b64encode(resp.content).decode()
        return f"data:{content_type};base64,{content}"


def get_background_image(el):
    url = el.attrib['style'].split(':', maxsplit=1)[1].strip()[5:-2].replace(r'\/', '/')
    return download_icon(url)


def parse_content(el):
    parser = ArticleParser('*')
    fragments = parser.parse(el)
    fragments = parser.normalize(fragments)
    perex, content = split_article_to_perex_and_content(fragments, [340, 660])
    return {
        'perex': perex,
        'content': content
    }


def extend_facebook_link(source, guid, fb_user, keep_image, post_args, htmltree):
    post_args['source'] = source
    try:
        el = htmltree.cssselect('.userContentWrapper .clearfix img')[0]
        author_name = el.attrib['aria-label']
        icon = download_icon(el.attrib['src'])

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

            post_args.update(parse_content(message_el))

        post_args['attachments']['author'] = author
        post_args['title'] = None
        post_args['guid'] = guid
    except IndexError as e:
        print(e)
    return post_args


def extend_facebook_note(source, guid, post_args, htmltree):
    post_args['source'] = source
    try:
        el_icon = htmltree.cssselect('.fb_content .clearfix .lfloat div[style]')[0]
        el_userbox = el_icon.getparent().getparent()
        el_header = el_userbox.getparent()
        el_content = el_header.getparent().getchildren()[1]

        post_args['guid'] = guid
        post_args['title'] = el_header.getchildren()[1].text

        icon = get_background_image(el_icon)
        fb_user = None
        el_user = el_userbox.getchildren()[1].cssselect('a')[0]
        href = el_user.attrib['href']
        m = RE_FACEBOOK_ALERNATE.fullmatch(href)
        if m:
            fb_user = m.group(2)

        author = {
            'name': el_user.text,
            'image': icon
        }
        if fb_user:
            author['id'] = fb_user
            author['profile_url'] = f"https://www.facebook.com/{fb_user}"

        post_args['attachments']['author'] = author
        post_args.update(parse_content(el_content))
    except IndexError as e:
        print(e)
    return post_args


class FacebookImporter:
    DOMAIN = 'facebook.com'

    def match(self, url):
        m = RE_FACEBOOK_POST.fullmatch(url)
        if m:
            user = m.group(2)
            post_id = m.group(3)
            source = f"https://www.facebook.com/{user}/posts/{post_id}"
            guid = f'fb|{user}_{post_id}'

            url = source + '?_fb_noscript=1'
            extend_callback = partial(extend_facebook_link, source, guid, user, False)
            return (url, guid, extend_callback)

        m = RE_FACEBOOK_GROUP_POST.fullmatch(url)
        if m:
            group_id = m.group(2)
            post_id = m.group(3)
            source = f"https://www.facebook.com/groups/{group_id}/permalink/{post_id}"
            guid = f'fb|{group_id}_{post_id}'

            url = source + '?_fb_noscript=1'
            extend_callback = partial(extend_facebook_link, source, guid, None, False)
            return (url, guid, extend_callback)

        m = RE_FACEBOOK_PHOTO.fullmatch(url)
        if m:
            photo_id = m.group(1)
            source = f"https://www.facebook.com/photo.php?fbid={photo_id}"
            guid = f'fb|photo:{photo_id}'

            url = source + '&_fb_noscript=1'
            extend_callback = partial(extend_facebook_link, source, guid, None, True)
            return (url, guid, extend_callback)

        m = RE_FACEBOOK_PHOTOS_PHOTO.fullmatch(url)
        if m:
            user = m.group(2)
            album_id = m.group(3)
            post_id = m.group(4)
            source = f"https://www.facebook.com/{user}/photos/{album_id}/{post_id}"
            guid = f'fb|photo:{album_id}/{post_id}'

            url = source + '?_fb_noscript=1'
            extend_callback = partial(extend_facebook_link, source, guid, user, True)
            return (url, guid, extend_callback)

        m = RE_FACEBOOK_NOTE.fullmatch(url)
        if m:
            user_title = m.group(2)
            note_slug = m.group(3)
            note_id = m.group(4)
            source = f"https://www.facebook.com/notes/{user_title}/{note_slug}/{note_id}"
            guid = f'fb|note:{note_slug}/{note_id}'

            url = source + '?_fb_noscript=1'
            extend_callback = partial(extend_facebook_note, source, guid)
            return (url, guid, extend_callback)
