from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import re
from django.template.defaultfilters import slugify
register = template.Library()

@register.filter
def current_time(menu):
    menu = menu.replace(' ', '-')
    return menu


@register.filter
def urlify(s):

    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)

    return s