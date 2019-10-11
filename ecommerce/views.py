from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import FormView
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views.generic import TemplateView
from django.utils.translation import gettext as _

from django.db.models import Q
from categories.models import Size, Brand, Undercategory, Overcategory, Gender, Category, Condition
from .mixins import RequestFormAttachMixin
from .forms import ContactForm
from products.models import Product
from accounts.models import Wishlist
from operator import itemgetter
from categories.models import Brand

def test_page(request):
	return render(request, "categories/slidebar.html", {})

class AboutPageView(TemplateView):
	template_name = 'base/about_us.html'
	def get_context_data(self, *args, **kwargs):
		context=super(AboutPageView, self).get_context_data(*args, **kwargs)
	
		# elif self.request.session.get('language') == 'UA':
		# 	context['bazar'] = 'Базар'
		# 	context['marketplace'] = 'Маркетплейс'
		# 	context['authentic_slogan'] = 'Без фейків'
		# 	context['authentic_text'] = "Те, що відрізняє нас від інших: на SALT немає і ніколи не буде фейків. Фейки - це те, що робить онлайн-шопінг нестерпним. Індустрія підробок у сфері моди оцінюється в 600 млрд доларів. У той час, коли хтось заробляє величезні гроші, якість шопінгу для покупця погіршується. Але ми любимо шопінг. Напевно, навіть більше, ніж Ти. Нами рухає дуже проста мета зробити шопінг максимально приємним і безпечним. Тому на SALT ти можеш бути на 100% впевнена_ий, що здобуваєш оригінальну річ."
		# 	context['ai_slogan'] = 'Двухфакторна верифікація'
		# 	context['ai_text'] = 'На SALT діє двухфакторна верифікація продукту (звучить круто, правда?). Простими словами, кожен айтем перевіряється рівно два рази. Перший - відразу після завантаження. За лічені секунди наша модель Штучного Інтелекту привласнює продукту лейбл - фейк або оригінал. Модель думає швидко і поліпшується з кожним завантаженим айтемом (нейронні сіточки і все таке). А другий крок - це ретельний мануальний чек, що виконується нашими досвідченими експертами. Завдяки двухфакторной верифікації продукту жоден фейк не потрапить на SALT.'
		# 	context['minimalism_slogan'] = 'Краще менше, та краще'
		# 	context['minimalism_text'] = "Простота - це наш основний концепт. І це стосується не тільки мінімалістичного дизайну та інтуїтивного інтерфейсу. Ми хочемо, щоб наших покупців і продавців поважали. Тому на SALT немає і ніколи не буде настирливої ​​реклами і платного просування. ніяких банерів, спливаючих вікон і преміум-акаунтів. SALT - це ком'юніті, де дизайнерська і вулична мода набуває другий шанс. Річ знаходить свого нового власника без шкоди навколишньому середовищу. SALT при цьому лише виконує скромну роль посередника в цій нехитрій угоді"
		# else:
		context['bazar'] = _('Bazar')
		context['marketplace'] = _('Marketplace')
		context['authentic_slogan'] = _('No counterfeit')
		context['authentic_text'] = _("What makes SALT different from others? Well, we have a zero-fake-policy here. Fakes make online shopping unbearable. The countterfeit industry in fashion is valued around $600 billion. While someone makes tons of money, the quality of shopping for the customer is deteriorating. But we love shopping. Probably even more than you. So we set up a very simple goal -  to make shopping as pleasant and safe as possible. Therefore, on SALT you can be 100% sure that you are buying a nice authentic piece.")
		context['ai_slogan'] = _('2-step-verification')
		context['ai_text'] = _("SALT has two-factor product verification (sounds awesome, right?). In simple words, each item is checked exactly two times. The first one happens right after uploading. Just in a few seconds, our AI-model assigns a label to the product - fake or authentic. The model thinks fast and improves itself with each loaded item (neural networks and all that). And the second step is a thorough manual check performed by our experienced experts. Thanks to the two-factor verification of all items, no fake will get to SALT.")
		context['minimalism_slogan'] = _('Less is more')
		context['minimalism_text'] = _("Simplicity is our core concept. And it's not only limited in minimalistic design and intuitive interface of SALT. We want both buyers and sellers to feel respected. Therefore, there is no and never will be annoying ads and paid promotion on SALT. No banners, paid pop-ups or premium accounts. SALT is a community where designer and streetwear clothes take their second chance. The item finds its new owner without harming the environment. SALT acts as a modest mediator in this straightforward, but essential deal.")
		return context

class ContactPageView(LoginRequiredMixin, RequestFormAttachMixin, FormView):
	form_class = ContactForm
	template_name = 'contact/contact.html'

	def get_context_data(self, *args, **kwargs):
		context=super(ContactPageView, self).get_context_data(*args, **kwargs)
		context['user_email'] = self.request.user.email
		# if self.request.session.get('language') == 'RU':
		# 	context['title'] = 'Напиши нам'
		# 	context['button'] = 'Отправить'
		# elif self.request.session.get('language') == 'UA':
		# 	context['title'] = 'Напиши нам'
		# 	context['button'] = 'Надіслати'
		# else:
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
			# if self.request.session.get('language') == 'RU':
			# 	return JsonResponse({"message":"Спасибо"})
			# elif self.request.session.get('language') == 'UA':
			# 	return JsonResponse({"message":"Дякуємо"})
			# else:
			return JsonResponse({
				"message":_("Thank you"),
				"success_message":_("Success")
				})
			
		def form_invalid(self, form):
			errors = form.errors.as_json()
			if request.is_ajax():
				return HttpResponse(errors, status=400, content_type='application/json')

	
	def form_invalid(self, form):
		errors = form.errors.as_json()
		if request.is_ajax():
			return HttpResponse(errors, status=400, content_type='application/json')

def home_page(request):
	qs = Product.objects.all().authentic()
	mydict = {}
	for obj in qs: 
		mydict[obj] = Wishlist.objects.filter(product=obj).count()
	sorted_ = sorted(mydict, key=mydict.get, reverse=True)
	most_liked = sorted_[:50]
	context = {}
	context['qs'] = qs
	context['liked'] = most_liked
	brands = ['Gucci', 'Stone Island', 'Chanel', 'Prada', 'Louis Vuitton', 'Dolce & Gabbana', 'Yves Saint Laurent', 'Fendi', 'Burberry', 'Givenchy', 'Versace', 'Balenciaga', 'Giorgio Armani', 'C.P. Company', 'Calvin Klein', 'Balmain', 'Alexander Wang', 'Boss']
	to_send = []
	for i in brands: 
		to_send.append(Brand.objects.filter(brand_name=i).first())
	# brands_navbar_init = brands
	# brand_navbar_lookups = (Q(brand_name__iexact='nothing'))
	# for brand in brands_navbar_init:
	# 	brand_navbar_lookups = brand_navbar_lookups|(Q(brand_name__iexact=brand))
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
	context['popular_brands_'] = _('Popular designers:')

	# context['kids_navbar'] = 'Дiтi'
	# context['new_navbar'] = 'Свiже'
	# context['brand'] = 'Бренд'
	# context['why_sell'] = 'Підтримуй круговорот одягу в природі.'
	# context['why_buy'] = 'Знайди свій брендовий айтем швидко та без фейків.'
	# context['safe'] = 'Надійно'
	# context['why_safe'] = 'Завантажені речі перевіряються 24/7/365. На SALT немає фейків і кидал.'
	# context['modern'] = 'Сучасно'
	# context['why_modern'] = 'Ми використовуємо Штучний Інтелект, щоб виключати підробки з нашого каталогу.'
	# context['simple'] = 'Просто'
	# context['why_simple'] = "Наш інтуїтивний дизайн розроблений з любов'ю до простоти i мінімалізму."
	# context['read_more'] = 'Дізнайся більше'
	# context['go_to_account'] = 'Перейти в акаунт'
	# context['become_customer'] = 'Приєднуйся'
	# context['login_registration'] = 'Логін | Реєстрація'
	# context['trending'] = 'У тренді:'
	# context['see_all'] = 'Показати всі'
	# context['popular_brands'] = 'Популярні бренди:'


	return render(request, "home_page.html", context)

# def contact_page(request):
# 	contact_form=ContactForm(request or None)
# 	if request.POST:
# 		contact_form=ContactForm(request.POST or None)
# 	context = { 
# 		'user_email':request.user.email,
# 		'title':'Contact page',
# 		'form':contact_form
# 	}

# 	if contact_form.is_valid():
# 		context = {
						
# 						'email':contact_form.cleaned_data.get('email'),
# 						'content':contact_form.cleaned_data.get('content'),
# 						'sender_email':request.user

# 				}
# 		txt_ = get_template("contact/email/contact_message.txt").render(context)
# 		html_ = get_template("contact/email/contact_message.html").render(context)
# 		subject = str(contact_form.cleaned_data.get('email'))+' User Message'
# 		from_email = settings.DEFAULT_FROM_EMAIL
# 		recipient_list = [from_email]
# 		sent_mail=send_mail(
# 					subject,
# 					txt_,
# 					from_email,
# 					recipient_list,
# 					html_message=html_,
# 					fail_silently=False, 

# 					)
# 		if request.is_ajax():
# 			return JsonResponse({"message":"Thank you"})

# 	if contact_form.errors:
# 		errors = contact_form.errors.as_json()
# 		if request.is_ajax():
# 			return HttpResponse(errors, status=400, content_type='application/json')
# 	# if request.method =="POST":
# 	# 	print(request.POST)
# 	return render(request, "contact/contact.html", context)






