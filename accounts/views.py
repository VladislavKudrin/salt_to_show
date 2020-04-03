from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.core.urlresolvers import reverse
from django.views.generic import FormView, DetailView, View, ListView
from django.views.generic.edit import FormMixin
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.utils import translation
from django.contrib import messages

from ecommerce.mixins import NextUrlMixin, RequestFormAttachMixin
from .models import EmailActivation, User, Wishlist, LanguagePreference
from .forms import *
from products.models import Product
from addresses.models import Address
from addresses.forms import AddressForm
from billing.models import BillingProfile, Card
from billing.forms import CardForm
from ecommerce.utils import add_message, custom_render


def region_init(request):
	if request.is_ajax():
		user = request.user
		if user.is_authenticated() and not user.region:
			form = RegionModalForm(request.POST, request=request)
			context = {
				'form': form,
				'path':request.GET.get('location')
			}
			html_ = get_template("accounts/snippets/region-modal/region-modal.html").render(request = request, context=context)
			json_data={
			'html':html_
			}
			return JsonResponse(json_data)
	if request.POST:
		user = request.user
		form = RegionModalForm(request.POST, request = request)
		if form.is_valid():
			form.save()
			# for updating language in mailchimp ------------
			# mark_pref, created = MarketingPreference.objects.get_or_create(user=user)
			# if mark_pref.subscribed == True: 
			# 	print('Views, if True')
			# 	response_status, response = Mailchimp().change_subscription_status(user.email, 'subscribed')
			# elif mark_pref.subscribed == False:
			# 	print('Views, if True')	
			# 	response_status, response = Mailchimp().change_subscription_status(user.email, 'unsubscribed')
			return redirect(form.cleaned_data.get('location'))
	return HttpResponse('html')
				 
def languge_pref_view(request):
	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirect_path=next_ or next_post or None
	language = request.GET.get('language')
	request.session['language'] = language
	if request.user.is_authenticated():
		user = request.user
		qs_lang = LanguagePreference.objects.filter(user=user)
		if qs_lang.exists():
			LanguagePreference.objects.update(user=user, language=language.lower())
		else:
			LanguagePreference.objects.create(user=user, language=language.lower())
		if is_safe_url(redirect_path, request.get_host()):
			return redirect(redirect_path)
	return redirect(redirect_path)

class AccountEmailActivateView(RequestFormAttachMixin, FormMixin, View):
	error_css_class = 'error'
	success_url='/login/'
	form_class=ReactivateEmailForm
	key = None
	def get(self, request, key=None, *args, **kwargs):
		self.key = key
		if key is not None:
			qs = EmailActivation.objects.filter(key__iexact=key)
			confirm_qs = qs.confirmable()
			if confirm_qs.count()==1:
				obj = confirm_qs.first()
				obj.activate()
				messages.add_message(request, messages.SUCCESS, _("You're in"))
				email = qs.first().user.email
				password = qs.first().user.password
				login(request, qs.first().user, backend='django.contrib.auth.backends.ModelBackend') 
				return redirect("accounts:home")
			else:
				activated_qs = qs.filter(activated=True)
				if activated_qs.exists():
					reset_link = reverse("password_reset")
					msg = _("""Your email has already been confirmed. Do you need to <a href="{link}">reset your password</a>?""").format(link=reset_link)
					messages.add_message(request, messages.SUCCESS, mark_safe(msg))
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
		msg = _("""Activation link was sent. Check your Email!""")
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

class RegisterLoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
	error_css_class = 'error'
	form_class = RegisterLoginForm
	success_url = '/'
	default_next='/'

	def get_template_names(self):
		if self.request.user_agent.is_mobile: 
			return ['accounts/mobile/register-login.html']
		else:
			return ['accounts/desktop/register-login.html']

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return redirect('home')
		return super(RegisterLoginView, self).get(request, *args,**kwargs)
	def get_context_data(self, *args, **kwargs):
		context = super(RegisterLoginView, self).get_context_data(*args,**kwargs)
		context['title'] = _('Login | Register')
		context['or_option'] = _('Or')
		context['password_forgot'] = _('Forgot password?')
		return context

	def lang_pref_update(self, user):
		language_pref_login_page = translation.get_language()
		language_pref = LanguagePreference.objects.filter(user=user)
		if language_pref.exists():
			self.request.session[translation.LANGUAGE_SESSION_KEY] = language_pref.first().language
		else:
			self.request.session[translation.LANGUAGE_SESSION_KEY] = language_pref_login_page
			LanguagePreference.objects.create(user=user, language=language_pref_login_page)

	def form_valid(self, form):
		next_path = self.get_next_url()
		email_from_form = form.cleaned_data.get('email')
		user = authenticate(form.request, username=email_from_form, password=form.cleaned_data.get('password'))
		user_objects_exists = User.objects.filter(email=email_from_form).exists()
		not_confirmed_activation_exists = EmailActivation.objects.email_exists(email_from_form).exists()
		confirmed_activation_exists = EmailActivation.objects.confirmed_activation_exists(email_from_form).exists()

		# REGISTRATION
		if user_objects_exists is False:
			form.save()
			user_created = User.objects.filter(email=email_from_form).first()
			self.lang_pref_update(user_created)
			next_path = 'login'
			msg_check_mail = _("Please check your email to confirm your account. ") + form.cleaned_data.get('msg')
			messages.add_message(form.request, messages.SUCCESS, mark_safe(msg_check_mail))
			return redirect(next_path)
		
		# THERE ARE ONLY NOT CONFIRMED EMAIL ACTIVATION
		elif not_confirmed_activation_exists and not confirmed_activation_exists:
			next_path = 'login'
			msg_confirm_mail = _("Email not confirmed. ") + form.cleaned_data.get('msg')
			messages.add_message(form.request, messages.WARNING, mark_safe(msg_confirm_mail))
			return redirect(next_path)
		
		# WRONG PASSWORD
		elif user is None:
			next_path = 'login'
			msg_wrong_password = _("The password seems to be wrong. Try again!")
			messages.add_message(form.request, messages.WARNING, mark_safe(msg_wrong_password))
			return redirect(next_path)

		# LOGIN 	
		else:
			self.lang_pref_update(user)
			login(form.request, user)
			msg_login_success = ('Ох заживеееем!') if user.admin else _("You're in")
			messages.add_message(form.request, messages.SUCCESS, mark_safe(msg_login_success))				
			return redirect(next_path)

class ProfileView(DetailView):
	template_name = 'accounts/profile.html'

	def get_template_names(self):
		if self.request.user_agent.is_mobile: 
			return ['accounts/mobile/profile.html']
		else:
			return ['accounts/desktop/profile.html']

	def get_context_data(self, *args, **kwargs):
		username = self.kwargs.get('username')
		user  = User.objects.filter_by_username(username=username)
		context = super(ProfileView, self).get_context_data(*args,**kwargs)
		context['products'] = Product.objects.filter(user=user).authentic().available().active()
		return context

	def post(self, request, *args, **kwargs):
		next_ = request.POST.get('next', '/')
		username = self.kwargs.get('username')
		redirect_url = next_ + 'messages/' + username
		return HttpResponseRedirect(redirect_url)
	
	def get_object(self, *args, **kwargs): 
		username = self.kwargs.get('username')
		try:
			user_instance = User.objects.filter_by_username(username=username)
		except User.DoesNotExist:
			raise Http404("Not Found")
		return User.objects.filter_by_username(username=username)

class WishListView(LoginRequiredMixin, ListView):

	def get_template_names(self):
		if self.request.user_agent.is_mobile: 
			return ['accounts/mobile/wishlist.html']
		else:
			return ['accounts/desktop/wishlist.html']

	def get_queryset(self, *args, **kwargs):
		user = self.request.user
		wishes = Wishlist.objects.filter(user=user).available().order_by('-timestamp')
		wished_products = [wish.product for wish in wishes]
		return wished_products

	def get_context_data(self, *args, **kwargs):
		user = self.request.user
		wishes = Wishlist.objects.filter(user=user).available().order_by('-timestamp')
		wished_products = [wish.product for wish in wishes]
		context = super(WishListView, self).get_context_data(*args,**kwargs)
		context['wishes'] = wished_products
		return context

@login_required
def wishlistupdate(request):
	product_id=request.POST.get('product_id')
	user = request.user
	user_wishes = Wishlist.objects.filter(user = user)

	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
			
		except Product.DoesNotExist:
			print("Show message to user!")
			return redirect("accounts:wish-list")
		user_wishes_exist = user_wishes.filter(product=product_obj)
		if 	user_wishes_exist.exists():
			user.wishes.remove(product_obj)
			user_wishes_exist.first().delete()
			added = False
			user_wishes_exist=user_wishes.count()

		else:
			user.wishes.add(product_obj)
			Wishlist.objects.create(user=user, product=product_obj)
			added = True
			user_wishes_exist=user_wishes.count()
		product_likes = Wishlist.objects.filter(product=product_obj).count()
		if request.is_ajax():
			json_data={
				"added": added,
				"removed": not added,
				 "wishes_count": user_wishes_exist,
				 'product_likes': product_likes,
			}
			return JsonResponse(json_data, status=200)
	return redirect("accounts:wish-list")

class AccountUpdateView(LoginRequiredMixin, RequestFormAttachMixin, View):

	def get(self, request, *args, **kwargs):
		return custom_render(self.request, "accounts", "account-settings", self.get_context_data())

	def get_success_url(self):
		return reverse("accounts:user-update")

	def get_address(self):
		billing_profile, created = BillingProfile.objects.new_or_get(self.request)
		address, created = Address.objects.new_or_get(billing_profile)
		return address

	def get_card(self):
		billing_profile, created = BillingProfile.objects.new_or_get(self.request)
		card, created = Card.objects.new_or_get(billing_profile)
		return card

	def get_context_data(self, *args, **kwargs):
		context = {}
		context['user_form'] = UserDetailChangeForm(self.request, prefix='user_form', instance=self.get_object())
		context['address_form'] = AddressForm(self.request, prefix='address_form', instance=self.get_address())
		context['card_form'] = CardForm(self.request, prefix='card_form', instance=self.get_card())
		context['object'] = self.get_object()
		context['title'] = _('Update your details')
		context['password_btn'] = _('Change password')
		context['save_btn'] = _('Save')
		context['logout_btn'] = _('Logout')
		return context

	def get_object(self):
		self.object = self.request.user
		return self.request.user

	def form_valid(self, user_form, address_form, card_form):
		user_form.save(commit=True)
		address_form.save(commit=True)
		card_form.save(commit=True)
		return(HttpResponseRedirect(self.get_success_url()))

	def post(self, request, *args, **kwargs):
		user_form = UserDetailChangeForm(data=self.request.POST, files=self.request.FILES, request=self.request, prefix='user_form', instance=self.get_object())
		address_form = AddressForm(data=self.request.POST, request=self.request, prefix='address_form', instance=self.get_address())
		card_form = CardForm(data=self.request.POST, request=self.request, prefix='card_form', instance=self.get_card())
		if user_form.is_valid() and address_form.is_valid() and card_form.is_valid():
			return self.form_valid(user_form, address_form, card_form)
		return HttpResponseRedirect(self.get_success_url())