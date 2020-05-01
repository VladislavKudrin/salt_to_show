from django import template


register = template.Library()

@register.simple_tag(takes_context=True)
def count_user_notifications(context):
	user = context['request'].user
	if user.is_authenticated():
		unread_not = user.notification.all().filter(user=user, read=False).count()
		return unread_not