from django import template
import datetime

register = template.Library()

@register.filter
def print_timestamp(timestamp):
	return timestamp.strftime("%d.%m.%Y")