from django import template
register = template.Library()

@register.filter
def to_next_path(value):
	if '?' in value:
		link = value.split('?')[1]
		link = '?' + link
		return link 	
	return ''