from django.db.models import Q
from django.conf import settings
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView, ListView
from django.views.generic.edit import FormMixin
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.utils import translation
from ecommerce.mixins import NextUrlMixin, RequestFormAttachMixin
from .models import GuestEmail, EmailActivation, User, Wishlist, LanguagePreference
from .forms import *
from .signals import user_logged_in_signal
from products.models import Product
from marketing.utils import Mailchimp
from marketing.models import MarketingPreference
from addresses.models import Address
from ecommerce.utils import add_message
from billing.models import BillingProfile, Card


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
	default_next = "/"
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
				# if request.session.get('language')=='RU':
				# 	messages.add_message(request, messages.SUCCESS, 'Ты на сайте')
				# elif request.session.get('language')=='UA':
				# 	messages.add_message(request, messages.SUCCESS, 'Ти на сайті')
				# else:
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
	template_name = 'accounts/register.html'
	default_next='/'
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

	def form_valid(self, form):
		next_path = self.get_next_url()
		user = authenticate(form.request, username=form.cleaned_data.get('email'), password=form.cleaned_data.get('password'))
		user_objects = User.objects.filter(email=form.cleaned_data.get('email')).exists()
		link_sent2 = EmailActivation.objects.email_exists(form.cleaned_data.get('email')).exists()
		if user_objects is False:
			form.save()
			user_created = User.objects.filter(email=form.cleaned_data.get('email')).first()
			LanguagePreference.objects.create(user=user_created, language=translation.get_language())
			next_path = 'login'
			msg1 = _("Please check your email to confirm your account. ") + form.cleaned_data.get('msg')
			messages.add_message(form.request, messages.SUCCESS, mark_safe(msg1))
			return redirect(next_path)
		elif link_sent2:
			msg2 = _("Email not confirmed. ") + form.cleaned_data.get('msg')
			messages.add_message(form.request, messages.WARNING, mark_safe(msg2))
		elif user is None:
			next_path = 'login'
			msg3 = _("The password seems to be wrong. Try again!")
			messages.add_message(form.request, messages.WARNING, mark_safe(msg3))
			return redirect(next_path)
		else:
			language_pref_login_page = translation.get_language()
			login(form.request, user)
			language_pref = LanguagePreference.objects.filter(user=user)
			if language_pref.exists():
				self.request.session[translation.LANGUAGE_SESSION_KEY] = language_pref.first().language
			else:
				self.request.session[translation.LANGUAGE_SESSION_KEY] = language_pref_login_page
				LanguagePreference.objects.create(user=user, language=language_pref_login_page)
			messages.add_message(form.request, messages.SUCCESS, _("You're in"))				
		return redirect(next_path)

class ProfileView(DetailView):
	template_name = 'accounts/profile.html'

	def get_context_data(self, *args, **kwargs):
		username = self.kwargs.get('username')
		user  = User.objects.filter_by_username(username=username)
		context = super(ProfileView, self).get_context_data(*args,**kwargs)
		context['products'] = Product.objects.filter(user=user).authentic()
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
	template_name = 'accounts/wish-list.html'


	def get_queryset(self, *args, **kwargs):
		user = self.request.user
		wishes = Wishlist.objects.filter(user=user).order_by('-timestamp')
		wished_products = [wish.product for wish in wishes]
		# pk_wishes = [x.pk for x in wishes] #['1', '3', '4'] / primary key list
		return wished_products
		#context = super(WishListView, self).get_context_data(*args,**kwargs)
		# all_wishes = user.wishes_user.all()
		# wished_products = []
		# for wish in all_wishes: 
		# 	wished_products.append(wish.product)
		# print(wished_products)
		# return wished_products
		# return Product.objects.filter()

	def get_context_data(self, *args, **kwargs):
		user = self.request.user
		wishes = Wishlist.objects.filter(user=user).order_by('-timestamp')
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

class AccountUpdateView(LoginRequiredMixin, RequestFormAttachMixin, UpdateView): 
	form_class = AccountMultiForm
	template_name='accounts/account-update-view.html'

	def get_object(self):
		return self.request.user

	def get_address(self):
		return Address.objects.filter(billing_profile__user=self.object).first()

	def get_card(self):
		return Card.objects.filter(billing_profile__user=self.object).first()

	def get_success_url(self):
		return reverse("accounts:user-update")

	def form_valid(self, form):
		user_form = form['user_form'].save()
		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(self.request)
		profile = form['address_form'].save(commit=False)
		profile.billing_profile = billing_profile
		profile.save()
		card_form = form['card_form'].save()
		return super(AccountUpdateView, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(AccountUpdateView, self).get_context_data(*args,**kwargs)
		context['title'] = _('Update your details')
		context['password_btn'] = _('Change password')
		context['save_btn'] = _('Save')
		context['logout_btn'] = _('Logout')
		return context

	def get_form_kwargs(self):
		kwargs = super(AccountUpdateView, self).get_form_kwargs()
		kwargs.update(instance={
		    'user_form': self.object,
		    'address_form': self.get_address(),
		    'card_form': self.get_card(),
		})
		return kwargs



