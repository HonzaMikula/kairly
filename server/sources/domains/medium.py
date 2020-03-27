import re
from functools import partial

RE_MEDIUM = re.compile(r'https://medium.com/([^/]+)/([^/]+)-(\w+)/?(\?.*)?')


def extend_medium_link(medium_user, guid, post_args, htmltree):
    post_args['guid'] = guid

    try:
        el_icon = htmltree.cssselect('article a[rel=noopener] > img[width="48"]')[0]
        author = {
            'id': medium_user,
            'profile_url': 'https://medium.com/' + medium_user,
            'name': el_icon.attrib['alt'],
            'image': el_icon.attrib['src']
        }
        post_args['attachments']['author'] = author
    except IndexError as e:
        print(e)
    return post_args


class MediumImporter:
    DOMAIN = 'medium.com'

    def match(self, url):
        m = RE_MEDIUM.fullmatch(url)
        if m:
            medium_user = m.group(1)
            post_id = m.group(3)
            guid = f'medium|{medium_user}/{post_id}'
            extend_callback = partial(extend_medium_link, medium_user, guid)
            return (url, guid, extend_callback)
