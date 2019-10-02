from django import template
import datetime
import django.utils.timesince 
from django.utils import timezone

register = template.Library()

@register.filter
def print_timestamp(timestamp):
	return timestamp.strftime("%a %H:%M").upper()


	
	
	

