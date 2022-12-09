import markdown
from django import template
from django.utils.safestring import mark_safe
#마크다운
register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg


@register.filter
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))