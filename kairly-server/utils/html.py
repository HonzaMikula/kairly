import bleach

ALLOWED_TAGS = [
  'a', 'abbr', 'acronym', 'b', 'br', 'blockquote', 'code', 'div', 'em',
  'h2', 'h3', 'h4',
  'i', 'img',
  'li', 'ol', 'p', 'span', 'strong', 'u', 'ul'
]
ALLOWED_ATTRIBUTES = {
  'a': ['href', 'title'],
  'abbr': ['title'],
  'acronym': ['title'],
  'img': ['src', 'alt', 'title', 'width', 'height']
}


def sanitize(text):
    return bleach.clean(text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
