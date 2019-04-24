from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.views.generic import UpdateView, View
from django.shortcuts import render, redirect


from .mixins import CsrfExemptMixin
from .utils import Mailchimp
from .forms import MarketingPreferenceForm
from .models import MarketingPreference


MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)


class MailChimpWebhookView(CsrfExemptMixin, View):
	def get(self, request, *args, **kwargs):
		return HttpResponse("Thank you", status=200)
	def post(self, request, *args, **kwargs):
		data = request.POST
		list_id = data.get('data[list_id]')
		if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
			hook_type = data.get('type')

			email = data.get('data[email]')
			response_status, response = Mailchimp().check_subscription_status(email)
			sub_status = response['status']
			is_subbed = None
			mailchimp_subbed = None
			if sub_status == "subscribed":
				is_subbed, mailchimp_subbed = (True, True)
			elif sub_status == "unsubscribed":
				is_subbed, mailchimp_subbed = (False, False)
			if is_subbed is not None and mailchimp_subbed is not None:
				qs = MarketingPreference.objects.filter(user__email__iexact=email)
				if qs.exists():
					qs.update(
						subscribed=is_subbed, 
						mailchimp_subscribed=mailchimp_subbed, 
						mailchimp_msg = str(data)
						)
					
		return HttpResponse("Thank you", status=200)




class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
	form_class = MarketingPreferenceForm
	template_name = 'base/forms.html'
	success_url = '/settings/email/'
	success_message = 'Your Email pref had been updated!'

	def dispatch(self, *args, **kwargs): #грубо говоря, рендер, последний метод, который выводит класс
		user = self.request.user
		if not user.is_authenticated():
			return redirect("/login/?next=/settings/email/")#HttpResponse("Not Allowed", status=400)
		return super(MarketingPreferenceUpdateView, self).dispatch(*args,**kwargs)
	def get_context_data(self, *args, **kwargs):
		context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update Email Preferences'
		return context

	def get_object(self):
		user = self.request.user
		obj, created = MarketingPreference.objects.get_or_create(user=user)
		return obj

'''
POST Method
data[merges][FNAME]:
data[web_id]: 23870859
data[email_type]: html
data[action]: unsub
data[email]: hello@teamcfe.com
data[merges][ADDRESS]:
data[merges][BIRTHDAY]:
data[merges][LNAME]:
data[id]: e391266ed6
type: unsubscribe
data[merges][PHONE]:
data[list_id]: 956c560eab
data[reason]: manual
fired_at: 2019-04-11 14:40:10
data[ip_opt]: 134.101.5.187
data[merges][EMAIL]: hello@teamcfe.com
'''

# def mailchimp_webhook_view(request):
# 	data = request.POST
# 	list_id = data.get('data[list_id]')
# 	if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
# 		hook_type = data.get('type')

# 		email = data.get('data[email]')
# 		response_status, response = Mailchimp().check_subscription_status(email)
# 		sub_status = response['status']
# 		is_subbed = None
# 		mailchimp_subbed = None
# 		if sub_status == "subscribed":
# 			is_subbed, mailchimp_subbed = (True, True)
# 		elif sub_status == "unsubscribed":
# 			is_subbed, mailchimp_subbed = (False, False)
# 		if is_subbed is not None and mailchimp_subbed is not None:
# 			qs = MarketingPreference.objects.filter(user__email__iexact=email)
# 			if qs.exists():
# 				qs.update(
# 					subscribed=is_subbed, 
# 					mailchimp_subscribed=mailchimp_subbed, 
# 					mailchimp_msg = str(data)
# 					)
		 
# 	return HttpResponse("Thank you", status=200)












