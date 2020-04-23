from django import template


register = template.Library()

@register.simple_tag(takes_context=True)
def get_user_region(context):
	user = context['request'].user
	if user.is_authenticated():
		return user.region
	else:
		return None

@register.simple_tag(takes_context=True)
def get_user_wishlist(context):
	user = context['request'].user
	if user.is_authenticated():
		return user.wishes.all()
	else:
		return None