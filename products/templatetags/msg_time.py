from django import template
import datetime
import django.utils.timesince 
from django.utils import timezone
from datetime import datetime
from django.utils.translation import gettext as _ 

register = template.Library()

@register.filter
def print_timestamp(timestamp):
	today_word = _('Today')
	yesterday_word = _('Yesterday')

	stamp = timestamp.date()
	today = datetime.today().date()

	if stamp == today:
		return timestamp.strftime(f"{today_word} %H:%M").upper()
	elif (today - stamp).days == 1:  
		return timestamp.strftime(f"{yesterday_word} %H:%M").upper()
	else: 
		return timestamp.strftime("%d/%m %H:%M").upper()


	
	
	

