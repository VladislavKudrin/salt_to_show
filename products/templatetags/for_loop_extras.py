from django import template

register = template.Library()

@register.filter
def to_none(value):
    return ""