from django.http import Http404
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.views.generic.edit import FormMixin
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect

from ecommerce.mixins import NextUrlMixin, RequestFormAttachMixin
from .models import GuestEmail, EmailActivation, User
from .forms import LoginForm, RegisterForm, GuestForm, ReactivateEmailForm, UserDetailChangeForm
from .signals import user_logged_in_signal


# @login_required
# def account_home_view(request):
# 	render(request, "accounts/home.html", {})


class AccountHomeView(LoginRequiredMixin, DetailView):  #default accounts/login
	template_name = 'accounts/home.html' 
	def get_object(self):
		return self.request.user

class AccountEmailActivateView(FormMixin, View):
	success_url='/login/'
	form_class=ReactivateEmailForm
	def get(self, request, key=None, *args, **kwargs):
		self.key = key
		if key is not None:
			qs = EmailActivation.objects.filter(key__iexact=key)
			confirm_qs = qs.confirmable()
			if confirm_qs.count()==1:
				obj = confirm_qs.first()
				obj.activate()
				messages.success(request, "Your Email has been confirmed. Please login.")
				return redirect("login")
			else:
				activated_qs = qs.filter(activated=True)
				if activated_qs.exists():
					reset_link = reverse("password_reset")
					msg = """Your Email has already been confirmed
					Do you need to <a href="{link}">reset your password</a>?
					""".format(link=reset_link)
					messages.success(request,mark_safe(msg))
					return redirect("login")
		context={
			'form': self.get_form(),
			'key': key
			}
		return render(request, 'registration/activation-error.html', context)

	def post(self, request, *args, **kwargs):
		#create form to activate an email
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		msg = """Activation link send. Check your Email!"""
		request = self.request
		messages.success(request, msg)
		email=form.cleaned_data.get("email")
		obj = EmailActivation.objects.email_exists(email).first()
		user = obj.user
		new_activation = EmailActivation.objects.create(user=user, email=email)
		new_activation.send_activation()
		return super(AccountEmailActivateView, self).form_valid(form)

	def form_invalid(self, form):
		context={
			'form': form,
			'key': self.key
		}
		return render(self.request, 'registration/activation-error.html', context)



class GuestRegisterView(NextUrlMixin, RequestFormAttachMixin, CreateView):
	form_class = GuestForm
	default_next = '/register/'

	def get_success_url(self):
		return self.get_next_url()

	def form_invalid(self, form):
		return redirect('/register/')

	# def form_valid(self, form):
	# 	request = self.request
	# 	email = form.cleaned_data.get("email")
	# 	new_guest_email = GuestEmail.objects.create(email=email)
	# 	request.session['guest_email_id'] = new_guest_email.id
	# 	return redirect(self.get_next_url())


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
	form_class = LoginForm
	success_url = '/'
	template_name = 'accounts/login.html'
	default_next='/'

	def form_valid(self, form):
		next_path = self.get_next_url()
		return redirect(next_path)


# def login_page(request):
# 	form = LoginForm(request.POST or None)
# 	context ={

# 		'form':form

# 	}
# 	#print(request.user.is_authenticated())

# 	next_ = request.GET.get('next')
# 	next_post = request.POST.get('next')
# 	redirect_path=next_ or next_post or None
# 	if form.is_valid():
# 		username = form.cleaned_data.get("username")
# 		password = form.cleaned_data.get("password")		
# 		user = authenticate(request, username=username, password=password)
# 		if user is not None:
# 			login(request, user)
# 			try:
# 				del request.session['guest_email_id']
# 			except:
# 				pass
# 			if is_safe_url(redirect_path, request.get_host()):
# 				return redirect(redirect_path)
# 			else:
# 				return redirect("/")
# 		else:
# 			print("Error")
	        
# 	return render(request, "accounts/login.html", context)

# #User = get_user_model()


class RegisterView(CreateView):
	form_class = RegisterForm
	template_name = 'accounts/register.html'
	success_url = '/login/'

class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
	form_class = UserDetailChangeForm
	template_name='accounts/detail-update-view.html'
	def get_object(self):
		return self.request.user

	def get_context_data(self, *args, **kwargs):
		context = super(UserDetailUpdateView, self).get_context_data(*args,**kwargs)
		context['title'] = 'Change Your Details'
		return context

	def get_success_url(self):
		return reverse("accounts:user-update")


# def register_page(request):
# 	form = RegisterForm(request.POST or None)
# 	context ={
# 		'form' : form
# 	}
# 	if form.is_valid():
# 		form.save()
# 	return render(request, "accounts/register.html", context)


class ProfileView(DetailView):
	template_name = 'accounts/profile.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ProfileView, self).get_context_data(*args,**kwargs)
		context['btn_title'] = 'Begin Chat with '
		return context

	def post(self, request, *args, **kwargs):
		next_ = request.POST.get('next', '/')
		username = self.kwargs.get('username')
		redirect_url = next_ + 'dialogs/' + username
		return HttpResponseRedirect(redirect_url)
	
	def get_object(self, *args, **kwargs):
		username = self.kwargs.get('username')
		try:
			user_instance = User.objects.filter_by_username(username=username)
		except User.DoesNotExist:
			raise Http404("Not Found")
		return User.objects.filter_by_username(username=username)











