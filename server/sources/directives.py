import shlex
import re

from django.core.exceptions import ValidationError


class SkipDirective:
    """Usage: skip domain <domain_name>"""
    name = 'skip'

    def __init__(self, target=None, value=None):
        if target != 'domain':
            raise ValueError("Target must be 'domain'. " + self.__doc__)
        if value is None:
            raise ValueError("Domain must be set." + self.__doc__)
        self.target = target
        self.value = value


class ReplaceDirective:
    """Usage: replace title <pattern> <replacement>"""
    name = 'replace'

    def __init__(self, target=None, pattern=None, replacement=None):
        if target not in ['title', 'document']:
            raise ValueError("Target must be 'title' or 'document'. " + self.__doc__)
        if pattern is None:
            raise ValueError("Pattern must be set." + self.__doc__)
        if replacement is None:
            raise ValueError("Replacement must be set." + self.__doc__)
        self.target = target
        self.pattern = re.compile(pattern)
        self.replacement = replacement

    def replace(self, title):
        return self.pattern.sub(self.replacement, title)


DIRECTIVES = {
    SkipDirective.name: SkipDirective,
    ReplaceDirective.name: ReplaceDirective,
}


def parse(conf):
    directives = []
    for line in conf.splitlines():
        line = line.strip()
        if not line or line[0] == '#':
            continue

        name, *args = shlex.split(line)

        try:
            cls = DIRECTIVES[name]
        except KeyError:
            raise ValueError(f"Unknow directive {name}")

        directives.append(cls(*args))
    return directives


def validate_directives(value):
    try:
        parse(value)
    except Exception as e:
        raise ValidationError(str(e)) from e
