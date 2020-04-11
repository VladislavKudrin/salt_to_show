from django import template
register = template.Library()

@register.filter
def get_chat_options(value):
	if settings.CHAT_WITH_PRODUCTS:
		return settings.CHAT_WITH_PRODUCTS
	else:
		return 'exclude'