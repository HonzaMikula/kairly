import re
from functools import partial

RE_THEREADERAPP = re.compile(r'https://threadreaderapp.com/thread/(\d+).html(\?.*)?')


def extend_thereaderapp_link(guid, post_args, htmltree):
    post_args['guid'] = guid
    post_args['title'] = None
    try:
        el_user_name = htmltree.cssselect('.box-user .username a')[0]
        el_user_link = htmltree.cssselect('.box-user .avatar a')[0]
        el_user_img = el_user_link.cssselect('img')[0]
        profile_url = el_user_link.attrib['href']

        author = {
            'id': profile_url.split('/')[-1],
            'profile_url': profile_url,
            'name': el_user_name.text.strip(),
            'image': el_user_img.attrib['src']
        }

        del post_args['attachments']['image']
        post_args['attachments']['author'] = author
    except IndexError as e:
        print(e)
    return post_args


class TheReaderAppImporter:
    DOMAIN = 'thereaderapp.com'

    def match(self, url):
        m = RE_THEREADERAPP.fullmatch(url)
        if m:
            thread_id = m.group(1)
            guid = f'thereaderapp|{thread_id}'
            extend_callback = partial(extend_thereaderapp_link, guid)
            return (url, guid, extend_callback)
