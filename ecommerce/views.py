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



from categories.models import Brand, Undercategory, Overcategory, Gender, Category
from .mixins import RequestFormAttachMixin
from .forms import ContactForm
from products.models import Product
from accounts.models import Wishlist
from .utils import get_data_from_novaposhta_api, my_render


def test_page(request):
	return render(request, "categories/slidebar.html", {})

class AboutPageView(TemplateView):
	template_name = 'base/about_us.html'
	def get_context_data(self, *args, **kwargs):
		context=super(AboutPageView, self).get_context_data(*args, **kwargs)
		context['bazar'] = _('Bazar')
		context['marketplace'] = _('Marketplace')
		context['authentic_slogan'] = _('No counterfeit')
		context['authentic_text'] = _("What makes SALT different from others? Well, we have a zero-fake-policy here. Fakes make online shopping unbearable. The countterfeit industry in fashion is valued around $600 billion. While someone makes tons of money, the quality of shopping for the customer is deteriorating. But we love shopping. Probably even more than you. So we set up a very simple goal - to make shopping as pleasant and safe as possible. Therefore, on SALT you can be %s%% sure that you are buying a nice authentic piece.") % 100
		context['ai_slogan'] = _('2-step-verification')
		context['ai_text'] = _("SALT has two-factor product verification (sounds awesome, right?). In simple words, each item is checked exactly two times. The first one happens right after uploading. Just in a few seconds, our AI-model assigns a label to the product - fake or authentic. The model thinks fast and improves itself with each loaded item (neural networks and all that). And the second step is a thorough manual check performed by our experienced experts. Thanks to the two-factor verification of all items, no fake will get to SALT.")
		context['minimalism_slogan'] = _('Less is more')
		context['minimalism_text'] = _("Simplicity is our core concept. And it's not only limited in minimalistic design and intuitive interface of SALT. We want both buyers and sellers to feel respected. Therefore, there is no and never will be annoying ads and paid promotion on SALT. No banners, paid pop-ups or premium accounts. SALT is a community where designer and streetwear clothes take their second chance. The item finds its new owner without harming the environment. SALT acts as a modest mediator in this straightforward, but essential deal.")
		return context

class PrivacyPageView(TemplateView):
	template_name = 'base/privacy.html'
	def get_context_data(self, *args, **kwargs):
		context=super(PrivacyPageView, self).get_context_data(*args, **kwargs)
		return context

class TermsPageView(TemplateView):
	template_name = 'base/terms.html'
	def get_context_data(self, *args, **kwargs):
		context=super(TermsPageView, self).get_context_data(*args, **kwargs)
		return context

class FAQPageView(TemplateView):
	template_name = 'base/faq.html'
	def get_context_data(self, *args, **kwargs):
		context=super(FAQPageView, self).get_context_data(*args, **kwargs)
		return context

class ContactPageView(LoginRequiredMixin, RequestFormAttachMixin, FormView):
	form_class = ContactForm
	template_name = 'contact/contact.html'
	def post(self, request, *args, **kwargs):
		order_id = request.POST.get('order_id_report')
		if order_id:
			request.session['order_id'] = order_id
			context = self.get_context_data()
			context['form'] = ContactForm(request, order_id)
			return render(self.request, self.template_name, context)
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
		txt_ = get_template("contact/email/contact_message.txt").render(context)
		html_ = get_template("contact/email/contact_message.html").render(context)
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

def my_render(request, *args, **kwargs):
    template_location = args[0]
    args_list = list(args)
    if request.user_agent.is_mobile:
        args_list[0] = 'mobile/' + template_location
        args = tuple(args_list)
        return render(request, *args, **kwargs)
    else:
        args_list[0] = 'desktop/' + template_location
        args = tuple(args_list)
        return render(request, *args, **kwargs)

def home_page(request):
	template_name =  'home_page.html'
	if request.user_agent.is_mobile:
		template = 'mobile/' + template_name
		context = {}
		return render(request, template, context)
	else:
		template = 'desktop/' + template_name
		qs = Product.objects.all().authentic()
		mydict = {}
		for obj in qs: 
			mydict[obj] = Wishlist.objects.filter(product=obj).count()
		sorted_ = sorted(mydict, key=mydict.get, reverse=True)
		most_liked = sorted_[:50]
		context = {}
		context['qs'] = qs
		context['liked'] = most_liked
		brands = ['Gucci', 'Stone Island', 'Chanel', 'Prada', 'Louis Vuitton', 'Dolce & Gabbana', 'Yves Saint Laurent', 'Fendi', 'Burberry', 'Givenchy', 'Versace', 'Balenciaga', 'Armani', 'C.P. Company', 'Comme des Garcons', 'Calvin Klein', 'Balmain', 'Alexander Wang']
		to_send = []
		for i in brands: 
			to_send.append(Brand.objects.filter(brand_name=i).first())
		context['showed_brands_navbar'] = to_send
		context['gender_navbar_adults'] = Gender.objects.filter(gender_for=Overcategory.objects.get(overcategory='Adults'))
		context['gender_navbar_kids'] = Gender.objects.filter(gender_for=Overcategory.objects.get(overcategory='Kids'))
		context['fields_gender'] = Gender.objects.all()
		context['fields_category'] = Category.objects.all()
		context['fields_overcategory'] = Overcategory.objects.all()
		context['fields_undercategory'] = Undercategory.objects.all()
		context['barabek'] = 'eaten'
		context['brands'] = to_send
		#translation
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
		return render(request, template, context)
	    


class MyCronJob(CronJobBase):
	RUN_EVERY_MINS = 0.01 # every 2 hours
	MIN_NUM_FAILURES = 1
	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'my_app.my_cron_job'    # a unique code

	def do(self):
		now = datetime.now(timezone.utc)
		time_from = now - timedelta(hours=8)
		# time_from = now # for testing 
		unread_notif = Notification.objects.filter(read=False, message__timestamp__lte=time_from)
		

		# ---- USER QUERYSET TO SEND EMAIL NOTIFICATIONS -----
		list_of_ids = []
		for i in unread_notif.values('user').distinct():
			my_id = list(i.values())[0]
			list_of_ids.append(my_id)
		users = User.objects.filter(pk__in=list_of_ids)

		# ----  SEND EMAIL NOTIFICATIONS -----
		subject = 'У тебя есть новые сообщения'
		from_email = settings.DEFAULT_FROM_EMAIL
		context = {}

		for user in users:
			email = user.email
			notif = unread_notif.filter(user=user)
			context['number_of_notif'] = notif.count()
			last_message = notif.last().message
			last_message_text = last_message.message
			last_message_from = last_message.user.username
			last_message_timestamp = last_message.user.timestamp
			context['last_message_text'] = last_message_text
			context['last_message_from'] = last_message_from
			context['last_message_timestamp'] = last_message_timestamp
			txt_ = get_template("registration/emails/notif.txt").render(context)
			html_ = get_template("registration/emails/notif.html").render(context)
			sent_mail=send_mail(
				subject,
				txt_,
				from_email,
				[email],
				html_message=html_,
				fail_silently=False, 
				)




class NovaPoshtaAPI(CronJobBase):
	RUN_EVERY_MINS = 1440 # 60*24 every 24 hours 
	# RUN_EVERY_MINS = 2 # for testing
	MIN_NUM_FAILURES = 1
	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'novaposhta'    # a unique code

	def do(self):
		get_data_from_novaposhta_api()
		send_mail('Cron Job Done', 'NovaPoshtaAPI successfully retrieved', settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])








