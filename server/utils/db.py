import re

from django.db.utils import IntegrityError


def get_column_if_duplicate(integrity_error):
    assert isinstance(integrity_error, IntegrityError)
    code, msg = integrity_error.args
    if code != 1062:
        return None
    m = re.match("Duplicate entry '(.*)' for key '(.*)'", msg)
    assert m
    return m.group(2)
