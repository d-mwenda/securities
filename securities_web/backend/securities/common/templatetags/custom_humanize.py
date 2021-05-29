import re

from django import template
from django.contrib.humanize.templatetags.humanize import intword


register = template.Library()

words = [
    ("million", "M"),
    ("billion", "B"),
    ("trillion", "T"),
]

@register.filter(is_safe=False)
def shortintword(value):
    value = intword(value)

    for word in words:
        try:
            if bool(re.search(word[0], value)):
                value = re.sub(word[0], word[1], value)
                break
        except TypeError:
            pass
    return value


