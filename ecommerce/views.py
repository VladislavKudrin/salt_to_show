from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import FormView
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings

from .mixins import RequestFormAttachMixin
from .forms import ContactForm
from django.contrib.auth.mixins import LoginRequiredMixin 
from products.models import Product
from accounts.models import Wishlist
from operator import itemgetter

def test_page(request):
	return render(request, "categories/slidebar.html", {})

def about_page(request):
	context = {}
	return render(request, "base/about_us.html", context)

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
	qs = Product.objects.all()
	mydict = {}
	for obj in qs: 
		mydict[obj] = Wishlist.objects.filter(product=obj).count()
	sorted_ = sorted(mydict, key=mydict.get, reverse=True)
	most_liked = sorted_[:50]
	context = {}
	context['qs'] = qs
	context['liked'] = most_liked
	if request.session.get('language') == 'RU':
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
	elif request.session.get('language') == 'UA':
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
	else:
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






