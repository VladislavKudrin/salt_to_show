from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import FormView
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse
from django_cron import CronJobBase, Schedule
from chat_ecommerce.models import Notification
from datetime import datetime, timezone, timedelta
from accounts.models import User
from django.utils.translation import gettext as _
from django.db.models import Count

from categories.models import Brand, Undercategory, Overcategory, Gender, Category
from .mixins import RequestFormAttachMixin
from .forms import ContactForm
from products.models import Product
from accounts.models import Wishlist
from .utils import get_data_from_novaposhta_api, custom_render


class AboutPageView(TemplateView):

	def get_template_names(self):
		if self.request.user_agent.is_mobile: 
			return ['mobile/about-us.html']
		else:
			return ['desktop/about-us.html']

	def get_context_data(self, *args, **kwargs):
		context=super(AboutPageView, self).get_context_data(*args, **kwargs)
		context['bazar'] = _('Bazar')
		context['marketplace'] = _('Marketplace')
		context['authentic_slogan'] = _('No counterfeit')
		context['ai_slogan'] = _('2-step-verification')
		context['minimalism_slogan'] = _('Less is more')
		return context

class PrivacyPageView(TemplateView):

	def get_template_names(self):
		if self.request.user_agent.is_mobile: 
			return ['mobile/privacy.html']
		else:
			return ['desktop/privacy.html']

	def get_context_data(self, *args, **kwargs):
		context=super(PrivacyPageView, self).get_context_data(*args, **kwargs)
		return context

class TermsPageView(TemplateView):

	def get_template_names(self):
		if self.request.user_agent.is_mobile: 
			return ['mobile/terms.html']
		else:
			return ['desktop/terms.html']

	def get_context_data(self, *args, **kwargs):
		context=super(TermsPageView, self).get_context_data(*args, **kwargs)
		return context

class FAQPageView(TemplateView):

	def get_template_names(self):
		if self.request.user_agent.is_mobile: 
			return ['mobile/faq.html']
		else:
			return ['desktop/faq.html']
	def get_context_data(self, *args, **kwargs):
		context=super(FAQPageView, self).get_context_data(*args, **kwargs)
		return context

class ContactPageView(LoginRequiredMixin, RequestFormAttachMixin, FormView):
	form_class = ContactForm

	def get_template_names(self):
		if self.request.user_agent.is_mobile:
			return ['mobile/contact.html']
		else:
			return ['desktop/contact.html']

	def post(self, request, *args, **kwargs):
		order_id = request.POST.get('order_id_report')
		if order_id:
			request.session['order_id'] = order_id
			context = self.get_context_data()
			context['form'] = ContactForm(request, order_id)
			return render(self.request, self.get_template_names(), context)
		else:
			return super(ContactPageView, self).post(request, *args, **kwargs)
	def get_context_data(self, *args, **kwargs):
		context=super(ContactPageView, self).get_context_data(*args, **kwargs)
		context['user_email'] = self.request.user.email
		context['title'] = _('Contact us')
		context['button'] = _('Submit')
		context['submitted'] = _('Sending....')
		return context

	def form_valid(self, form):
		context = {			
		'email':form.cleaned_data.get('email'),
		'content':form.cleaned_data.get('content'),
		'sender_email':self.request.user
		}
		txt_ = get_template("emails/contact_message.txt").render(context)
		html_ = get_template("emails/contact_message.html").render(context)
		subject = str(form.cleaned_data.get('email'))+' User Message'
		from_email = settings.DEFAULT_FROM_EMAIL
		recipient_list = [from_email]
		sent_mail=send_mail(
					subject,
					txt_,
					from_email,
					recipient_list,
					html_message=html_,
					fail_silently=False, 

					)
		if self.request.is_ajax():
			if self.request.session.get('order_id'):
				del self.request.session['order_id']
				return JsonResponse({
					"message":_("Thank you, your report has been sended"),
					"success_message":_("Success"),
					"report": True,
					"location": reverse('contact')
					})
			else:	
				return JsonResponse({
					"message":_("Thank you"),
					"success_message":_("Success")
					})

	def form_invalid(self, form):
		errors = form.errors.as_json()
		if self.request.is_ajax():
			return HttpResponse(errors, status=400, content_type='application/json')

def home_page(request):
	template_name =  'home-page.html'
	context = {}
	context['kids_navbar'] = _('Kids')
	context['new_navbar'] = _('New')
	context['brand'] = _('Brand')
	context['why_sell'] = _('Contribute to the sustainable clothes-circle.')
	context['why_buy'] = _('Find your designer piece fast and safe.')
	context['safe'] = _('Safe')
	context['why_safe'] = _('Uploaded items are monitored 24/7/365. There are no fakes on SALT.')
	context['modern'] = _('AI-Powered')
	context['why_modern'] = _('We use Machine Learning to detect fakes in our catalogue.')
	context['simple'] = _('Simple')
	context['why_simple'] = _('Our intuitive design was made with love to simplicity and minimalism.')
	context['read_more'] = _('Read more')
	context['go_to_account'] = _('Go to your profile')
	context['become_customer'] = _('Join our community')
	context['login_registration'] = _('Login | Registration')
	context['trending'] = _('Trending:')
	context['see_all'] = _('See all')
	context['popular_brands'] = _('Popular designers:')

	if request.user_agent.is_mobile:
		template = 'mobile/' + template_name

		# The top 4 products, in order by number of wishlist objects (=liked).
		qs = Product.objects.authentic().available().payable()
		most_liked = qs.annotate(num_likes=Count('wishes_products')).order_by('-num_likes')[:4] 
		# print([i.num_likes for i in most_liked]) # for test
		context['liked'] = most_liked

		# Send 16 brands and according links
		brands = [
		'Gucci', 'Stone Island', 'Prada', 'Acne Studios', 
		'Dolce & Gabbana', 'Yves Saint Laurent', 'Comme des Garcons', 'Burberry', 
		'Versace',  'Armani', 'C.P. Company', 'Fendi'
		]
		context['brands'] = Brand.objects.filter(brand_name__in=brands)

		return render(request, template, context)

	else:
		template = 'desktop/' + template_name
		qs = Product.objects.authentic().available().payable()
		mydict = {}
		most_liked = qs.annotate(num_likes=Count('wishes_products')).order_by('-num_likes')[:25] 
		context['qs'] = qs
		context['liked'] = most_liked
		brands = ['Gucci', 'Stone Island', 'Chanel', 'Prada', 'Louis Vuitton', 'Dolce & Gabbana', 'Yves Saint Laurent', 'Fendi', 'Burberry', 'Givenchy', 'Versace', 'Balenciaga', 'Armani', 'C.P. Company', 'Comme des Garcons', 'Calvin Klein', 'Balmain', 'Alexander Wang']
		brands_to_send = [Brand.objects.filter(brand_name=i).first() for i in brands]
		context['brands'] = brands_to_send
		context['showed_brands_navbar'] = brands_to_send
		context['gender_navbar_adults'] = Gender.objects.filter(gender_for=Overcategory.objects.get(overcategory='Adults'))
		context['gender_navbar_kids'] = Gender.objects.filter(gender_for=Overcategory.objects.get(overcategory='Kids'))
		context['fields_gender'] = Gender.objects.all()
		context['fields_category'] = Category.objects.all()
		context['fields_overcategory'] = Overcategory.objects.all()
		context['fields_undercategory'] = Undercategory.objects.all()
		return render(request, template, context)
	    
class MessagesNotifications(CronJobBase):
	RUN_EVERY_MINS = 1 # everysecond
	MIN_NUM_FAILURES = 1
	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'messages'    # a unique code

	def send_notifications(
		self,
		user,
		amount,
		last_message_text, 
		last_message_from, 
		last_message_timestamp):
		email = user.email 
		subject = 'У тебя есть новые сообщения'
		from_email = settings.DEFAULT_FROM_EMAIL
		context = {}
		context['number_of_notif'] = amount
		context['last_message_text'] = last_message_text
		context['last_message_from'] = last_message_from
		context['last_message_timestamp'] = last_message_timestamp	
		txt_ = get_template("emails/notif.txt").render(context)
		html_ = get_template("emails/notif.html").render(context)
		sent_mail=send_mail(
			subject,
			txt_,
			from_email,
			[email],
			html_message=html_,
			fail_silently=False, 
			)
		if sent_mail == 1: 
			return True
		return False

	def do(self):
		# ALL 
		unread_notif = Notification.objects.filter(read=False, sent=False) # all not read, not sent
		# LIST OF USERS
		list_of_ids = unread_notif.values_list('user', flat=True).distinct()
		users = User.objects.filter(pk__in=list_of_ids)

		# NOTIFICATIONS BY USER
		for user in users: 
			notifications = unread_notif.filter(user=user)
			amount = notifications.count()
			# LAST MESSAGE
			last_message = notifications.last().message
			last_message_text = last_message.message
			last_message_from = last_message.user.username
			last_message_timestamp = last_message.user.timestamp
			# SEND EMAIL
			sent = self.send_notifications(user, amount, last_message_text, last_message_from, last_message_timestamp)
			if sent: 
				notifications.update(sent=True)
			else: 
				print('Was not sent')

class NovaPoshtaAPI(CronJobBase):
	RUN_EVERY_MINS = 2880 # 60*24 every 48 hours 
	# RUN_EVERY_MINS = 2 # for testing
	MIN_NUM_FAILURES = 1
	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'novaposhta'    # a unique code

	def do(self):
		get_data_from_novaposhta_api()
		send_mail('Cron Job Done', 'NovaPoshtaAPI successfully retrieved', settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])








