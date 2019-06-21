from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import FormView
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings

from .mixins import RequestFormAttachMixin
from .forms import ContactForm


def test_page(request):
	return render(request, "categories/slidebar.html", {})



def about_page(request):
	context = {
		'title':'About Page',
		'content':'Welcome to the about page'
	}
	return render(request, "base/about_us.html", context)




class ContactPageView(RequestFormAttachMixin, FormView):
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
	return render(request, "home_page.html", {})

def home_page_old(request):
	html_ = """
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">

    <title>Hello, world!</title>
  </head>
  <body>
  <div class='text-center'>
    <h1>Hello, world!</h1>
  </div>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>
  </body>
</html>
	
	"""
	return HttpResponse(html_)






