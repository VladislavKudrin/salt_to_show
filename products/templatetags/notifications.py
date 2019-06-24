import datetime
from django import template
from chat_ecommerce.models import Notification

register = template.Library()

@register.filter
def get_notif(user):
	unread_not= Notification.objects.filter(user=user, read=False).count() 
	return unread_not