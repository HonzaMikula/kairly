import shlex

from django.core.exceptions import ValidationError


class SkipDirective:
    """Usage: skip domain [domain_name]"""
    name = 'skip'

    def __init__(self, target=None, value=None):
        if target != 'domain':
            raise ValueError("Target must be 'domain'. " + self.__doc__)
        if value is None:
            raise ValueError("Domain name is missing." + self.__doc__)
        self.target = target
        self.value = value


DIRECTIVES = {
    SkipDirective.name: SkipDirective
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
