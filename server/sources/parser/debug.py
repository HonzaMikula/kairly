import re
from functools import wraps

from .html import fragments_to_string

level = 0


def normalize_logging(normalize_element):
    def element_to_str(el):
        markup = fragments_to_string([el])
        return re.sub(r'\n\s*', '', markup)

    @wraps(normalize_element)
    def wrapper(el):
        global level
        indent = " " * level
        print("{}normalize_element({})".format(indent, element_to_str(el)))
        level += 1
        elements = normalize_element(el)
        level -= 1
        for el in elements:
            if isinstance(el, str):
                print("{}- str: {}".format(indent, el))
            else:
                print("{}- {}".format(indent, element_to_str(el)))
        return elements

    return wrapper
