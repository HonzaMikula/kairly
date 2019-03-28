from urllib.parse import urlsplit, urlunsplit, parse_qs, urlencode


def clean_url(url):
    u = urlsplit(url)
    query = parse_qs(u.query)
    query.pop('ref', None)
    query.pop('source', None)
    query.pop('utm_source', None)
    query.pop('utm_medium', None)
    query.pop('utm_campaign', None)
    query.pop('fbclid', None)
    query.pop('preview', None)
    query.pop('redirected', None)
    qs = urlencode(query)

    return urlunsplit(
        (u.scheme, u.netloc, u.path, qs, u.fragment)
    )
