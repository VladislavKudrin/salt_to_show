from django import template
register = template.Library()

@register.filter
def format_decimal(value):
	return format(value, '.0f')