from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import FormView
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views.generic import TemplateView


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
		if self.request.session.get('language') == 'RU':
			context['bazar'] = 'Базарррр'
			context['marketplace'] = 'Маркетплейс'
			context['authentic_slogan'] = 'Без фейков'
			context['authentic_text'] = "То, что отличает нас от других: на SALT нет и никогда не будет фейков. Фейки – это то, что делает онлайн-шопинг невыносимым. Индустрия подделок в сфере моды оценивается в 600 млрд долларов. В то время, как кто-то зарабатывает огромные деньги, качество шопинга для покупателя ухудшается. Но мы любим шопинг. Наверное, даже больше, чем Ты. Нами движет очень простая цель сделать шопинг максимально приятным и безопасным. Поэтому на SALT ты можешь быть на 100% уверен_а, что приобретаешь оригинальную вещь. "
			context['ai_slogan'] = 'Двухфакторная верификация'
			context['ai_text'] = 'На SALT действует двухфакторная верификация продукта (звучит круто, правда?). Простыми словами, каждый айтем проверяется ровно два раза. Первый – сразу после загрузки. За считанные секунды наша модель Искусственного Интеллекта присваивает продукту лейбл – фейк или оригинал. Модель думает быстро и улучшается с каждым загруженным айтемом (нейронные сети и все такое). А второй шаг – это тщательный мануальный чек, выполняемый нашими опытными экспертами. Благодаря двухфакторной верификации продукта ни один фейк не попадет на SALT. '
			context['minimalism_slogan'] = 'Лучше меньше, да лучше'
			context['minimalism_text'] = "Простота – это наш основной концепт. И это касается не только минималистичного дизайна и интуитивного интерфейса. Мы хотим, чтобы наших покупателей и продавцов уважали. Поэтому на SALT нет и никогда не будет назойливой рекламы и платного продвижения. Никаких баннеров, всплывающих окон и премиум-аккаунтов. SALT – это коммьюнити, где дизайнерская и уличная мода приобретает второй шанс. Вещь находит своего нового владельца без вреда окружающей среде. SALT при этом лишь выполняет скромную роль посредника в этой незамысловатой сделке."
		elif self.request.session.get('language') == 'UA':
			context['bazar'] = 'Базар'
			context['marketplace'] = 'Маркетплейс'
			context['authentic_slogan'] = 'Без фейків'
			context['authentic_text'] = "Те, що відрізняє нас від інших: на SALT немає і ніколи не буде фейків. Фейки - це те, що робить онлайн-шопінг нестерпним. Індустрія підробок у сфері моди оцінюється в 600 млрд доларів. У той час, коли хтось заробляє величезні гроші, якість шопінгу для покупця погіршується. Але ми любимо шопінг. Напевно, навіть більше, ніж Ти. Нами рухає дуже проста мета зробити шопінг максимально приємним і безпечним. Тому на SALT ти можеш бути на 100% впевнена_ий, що здобуваєш оригінальну річ."
			context['ai_slogan'] = 'Двухфакторна верифікація'
			context['ai_text'] = 'На SALT діє двухфакторна верифікація продукту (звучить круто, правда?). Простими словами, кожен айтем перевіряється рівно два рази. Перший - відразу після завантаження. За лічені секунди наша модель Штучного Інтелекту привласнює продукту лейбл - фейк або оригінал. Модель думає швидко і поліпшується з кожним завантаженим айтемом (нейронні сіточки і все таке). А другий крок - це ретельний мануальний чек, що виконується нашими досвідченими експертами. Завдяки двухфакторной верифікації продукту жоден фейк не потрапить на SALT.'
			context['minimalism_slogan'] = 'Less is more'
			context['minimalism_text'] = "Простота - це наш основний концепт. І це стосується не тільки мінімалістичного дизайну та інтуїтивного інтерфейсу. Ми хочемо, щоб наших покупців і продавців поважали. Тому на SALT немає і ніколи не буде настирливої ​​реклами і платного просування. ніяких банерів, спливаючих вікон і преміум-акаунтів. SALT - це ком'юніті, де дизайнерська і вулична мода набуває другий шанс. Річ знаходить свого нового власника без шкоди навколишньому середовищу. SALT при цьому лише виконує скромну роль посередника в цій нехитрій угоді"
		else:
			context['bazar'] = 'Bazar'
			context['marketplace'] = 'Marketplace'
			context['authentic_slogan'] = 'No counterfeit'
			context['authentic_text'] = "What makes SALT different from others? Well, we have a zero-fake-policy here. Fakes make online shopping unbearable. The countterfeit industry in fashion is valued around $600 billion. While someone makes tons of money, the quality of shopping for the customer is deteriorating. But we love shopping. Probably even more than you. So we set up a very simple goal -  to make shopping as pleasant and safe as possible. Therefore, on SALT you can be 100% sure that you are buying a nice authentic piece."
			context['ai_slogan'] = '2-step-verification'
			context['ai_text'] = "SALT has two-factor product verification (sounds awesome, right?). In simple words, each item is checked exactly two times. The first one happens right after uploading. Just in a few seconds, our AI-model assigns a label to the product - fake or authentic. The model thinks fast and improves itself with each loaded item (neural networks and all that). And the second step is a thorough manual check performed by our experienced experts. Thanks to the two-factor verification of all items, no fake will get to SALT."
			context['minimalism_slogan'] = 'Less is more'
			context['minimalism_text'] = "Simplicity is our core concept. And it's not only limited in minimalistic design and intuitive interface of SALT. We want both buyers and sellers to feel respected. Therefore, there is no and never will be annoying ads and paid promotion on SALT. No banners, paid pop-ups or premium accounts. SALT is a community where designer and streetwear clothes take their second chance. The item finds its new owner without harming the environment. SALT acts as a modest mediator in this straightforward, but essential deal."
		return context

class ContactPageView(LoginRequiredMixin, RequestFormAttachMixin, FormView):
	form_class = ContactForm
	template_name = 'contact/contact.html'

	def get_context_data(self, *args, **kwargs):
		context=super(ContactPageView, self).get_context_data(*args, **kwargs)
		context['user_email'] = self.request.user.email
		if self.request.session.get('language') == 'RU':
			context['title'] = 'Напиши нам'
			context['button'] = 'Отправить'
		elif self.request.session.get('language') == 'UA':
			context['title'] = 'Напиши нам'
			context['button'] = 'Надіслати'
		else:
			context['title'] = 'Contact us'
			context['button'] = 'Submit'
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
			if self.request.session.get('language') == 'RU':
				return JsonResponse({"message":"Спасибо"})
			elif self.request.session.get('language') == 'UA':
				return JsonResponse({"message":"Дякуємо"})
			else:
				return JsonResponse({"message":"Thank you"})
			
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
	context['brands'] = to_send

	if request.session.get('language') == 'EN':
		context['kids_navbar'] = 'Kids'
		context['new_navbar'] = 'New'
		context['brand'] = 'Brand'
		context['why_sell'] = 'Contribute to the sustainable clothes-circle.'
		context['why_buy'] = 'Find your designer piece fast and safe.'
		context['safe'] = 'Safe'
		context['why_safe'] = 'Uploaded items are monitored 24/7/365. There are no fakes on SALT.'
		context['modern'] = 'AI-Powered'
		context['why_modern'] = 'We use Machine Learning to detect fakes in our catalogue.'
		context['simple'] = 'Simple'
		context['why_simple'] = 'Our intuitive design was made with love to simplicity and minimalism.'
		context['read_more'] = 'Read more'
		context['go_to_account'] = 'Go to your profile'
		context['become_customer'] = 'Join our community'
		context['login_registration'] = 'Login | Registration'
		context['trending'] = 'Trending:'
		context['see_all'] = 'See all'
		context['popular_brands'] = 'Popular designers:'
	elif request.session.get('language') == 'UA':
		context['kids_navbar'] = 'Дiти'
		context['new_navbar'] = 'Свiже'
		context['brand'] = 'Бренд'
		context['why_sell'] = 'Підтримуй круговорот одягу в природі.'
		context['why_buy'] = 'Знайди свій брендовий айтем швидко та без фейків.'
		context['safe'] = 'Надійно'
		context['why_safe'] = 'Завантажені речі перевіряються 24/7/365. На SALT немає фейків і кидал.'
		context['modern'] = 'Сучасно'
		context['why_modern'] = 'Ми використовуємо Штучний Інтелект, щоб виключати підробки з нашого каталогу.'
		context['simple'] = 'Просто'
		context['why_simple'] = "Наш інтуїтивний дизайн розроблений з любов'ю до простоти i мінімалізму."
		context['read_more'] = 'Дізнайся більше'
		context['go_to_account'] = 'Перейти в акаунт'
		context['become_customer'] = 'Приєднуйся'
		context['login_registration'] = 'Логін | Реєстрація'
		context['trending'] = 'У тренді:'
		context['see_all'] = 'Показати всі'
		context['popular_brands'] = 'Популярні бренди:'
	else:
		context['kids_navbar'] = 'Дети'
		context['new_navbar'] = 'Свежее'
		context['brand'] = 'Бренд'
		context['why_sell'] = 'Поддерживай круговорот одежды в природе.'
		context['why_buy'] = 'Найди свой брендовый айтем быстро и без фейков.'
		context['safe'] = 'Надежно'
		context['why_safe'] = 'Загруженные вещи проверяются 24/7/365. На SALT нет фейков и кидал.'
		context['modern'] = 'Современно'
		context['why_modern'] = 'Мы используем Искусственный Интеллект, чтобы исключать подделки из нашего каталога.'
		context['simple'] = 'Просто'
		context['why_simple'] = 'Наш интуитивный дизайн разработан с любовью к простоте и минимализму.'
		context['read_more'] = 'Узнай больше'
		context['go_to_account'] = 'Перейти в аккаунт'
		context['become_customer'] = 'Присоединяйся'
		context['login_registration'] = 'Логин | Регистрация'
		context['trending'] = 'В тренде:'
		context['see_all'] = 'Показать все'
		context['popular_brands'] = 'Популярные бренды:'
		


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






