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
	context = {
		'title':'About Page',
		'content':'Welcome to the about page'
	}
	return render(request, "base/about_us_3.html", context)




class ContactPageView(LoginRequiredMixin, RequestFormAttachMixin, FormView):
	form_class = ContactForm
	template_name = 'contact/contact.html'
	def get_context_data(self, *args, **kwargs):
		context=super(ContactPageView, self).get_context_data(*args, **kwargs)
		context['user_email'] = self.request.user.email
		context['title'] = 'Contact page'
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


def home_page(request):
	qs = Product.objects.all()
	mydict = {}
	for obj in qs: 
		mydict[obj] = Wishlist.objects.filter(product=obj).count()
	sorted_ = sorted(mydict, key=mydict.get, reverse=True)
	most_liked = sorted_[:50]
	context = {
		'qs': qs,
		'liked': most_liked,
	}
	return render(request, "home_page.html", context)



