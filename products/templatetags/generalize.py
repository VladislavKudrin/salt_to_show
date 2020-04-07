from django import template
register = template.Library()

@register.filter
def generalize(value):
	generalized = value.split(',')[0]
	return generalized