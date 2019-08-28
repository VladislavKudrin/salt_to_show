
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save

from .utils import Mailchimp
from accounts.models import Region, User

class MarketingPreference(models.Model):
	user 						= models.OneToOneField(settings.AUTH_USER_MODEL, related_name='marketing')
	subscribed 					= models.BooleanField(default=True)
	mailchimp_subscribed 		= models.NullBooleanField(default=True)
	mailchimp_msg 				= models.TextField(null=True, blank=True)
	timestamp 					= models.DateTimeField(auto_now_add=True)
	update 						= models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.email


def marketing_pref_create_reciever(sender, instance, created, *args, **kwargs):
	if created:
		status_code, response_data = Mailchimp().subscribe(instance.user.email)


post_save.connect(marketing_pref_create_reciever, sender=MarketingPreference)

def marketing_pref_update_reciever(sender, instance, *args, **kwargs):
	if instance.subscribed != instance.mailchimp_subscribed:
		if instance.subscribed:
			status_code, response_data = Mailchimp().subscribe(instance.user.email)
		else:
			status_code, response_data = Mailchimp().unsubscribe(instance.user.email)

		if response_data['status'] == 'subscribed':
			instance.subscribed = True
			instance.mailchimp_subscribed = True
			instance.mailchimp_msg = response_data
		else: 
			instance.subscribed = False
			instance.mailchimp_subscribed = False
			instance.mailchimp_msg = response_data

pre_save.connect(marketing_pref_update_reciever, sender=MarketingPreference)

def make_marketing_pref_reciever(sender, instance, created, *args, **kwargs):
	#print(MarketingPreference.objects.filter(user=instance).first().subscribed) #model and forms work just fine
	user = User.objects.filter(email=instance).first() 
	mark_pref, created = MarketingPreference.objects.get_or_create(user=user)
	if mark_pref.subscribed == True: 
		response_status, response = Mailchimp().change_subscription_status(user.email, 'subscribed')
	elif mark_pref.subscribed == False:	
		print('HUIIII')
		print(mark_pref.subscribed)
		response_status, response = Mailchimp().change_subscription_status(user.email, 'unsubscribed')


post_save.connect(make_marketing_pref_reciever, sender=settings.AUTH_USER_MODEL)





