
def parse_og_tags(htmltree):
    values = {}
    for meta in htmltree.cssselect('head meta'):
        prop = meta.attrib.get('property', '')
        if prop.startswith('og:'):
            values[prop[3:]] = meta.attrib.get('content')
    return values
