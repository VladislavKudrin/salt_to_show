from django import template


register = template.Library()

@register.simple_tag(takes_context=True)
def get_user_card(context):
	user = context['request'].user
	if user.is_authenticated():
		return user.billing_profile.default_card.first()
	else:
		return None
