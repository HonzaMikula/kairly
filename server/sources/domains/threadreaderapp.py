import re
from functools import partial

RE_THREAD_READER_APP = re.compile(r'https://threadreaderapp.com/thread/(\d+).html(\?.*)?')


def extend_thread_reader_link(guid, post_args, htmltree):
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


class ThreadReaderAppImporter:
    DOMAIN = 'thereaderapp.com'

    def match(self, url):
        m = RE_THREAD_READER_APP.fullmatch(url)
        if m:
            thread_id = m.group(1)
            guid = f'threadreaderapp|{thread_id}'
            extend_callback = partial(extend_thread_reader_link, guid)
            return (url, guid, extend_callback)
