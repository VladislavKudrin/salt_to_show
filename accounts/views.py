from django.db.models import Q
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView, ListView
from django.views.generic.edit import FormMixin
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe

from ecommerce.mixins import NextUrlMixin, RequestFormAttachMixin
from .models import GuestEmail, EmailActivation, User, Wishlist, LanguagePreference
from .forms import RegisterLoginForm, GuestForm, ReactivateEmailForm, UserDetailChangeForm
from .signals import user_logged_in_signal
from products.models import Product


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

class AccountHomeView(LoginRequiredMixin, DetailView):  #default accounts/login
	template_name = 'accounts/home.html' 
	def get_object(self):
		user=User.objects.check_username(self.request.user)
		return self.request.user

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
				if request.session.get('language')=='RU':
					messages.add_message(request, messages.SUCCESS, 'Ты на сайте')
				elif request.session.get('language')=='UA':
					messages.add_message(request, messages.SUCCESS, 'Ти на сайті')
				else:
					messages.add_message(request, messages.SUCCESS, "You're in")
				email = qs.first().user.email
				password = qs.first().user.password
				login(request, qs.first().user, backend='django.contrib.auth.backends.ModelBackend') 
				return redirect("accounts:home")
			else:
				activated_qs = qs.filter(activated=True)
				if activated_qs.exists():
					reset_link = reverse("password_reset")
					if request.session.get('language')=='RU':
						msg = """Ты уже подтвердил_а свой мейл. 
						<a href="{link}">Сбросить пароль</a>?
						""".format(link=reset_link)
					elif request.session.get('language')=='UA':
						msg = """Ти вже підтвердив/підтвердила свій мейл. 
						<a href="{link}">Скинути пароль</a>?
						""".format(link=reset_link)
					else:
						msg = """Your email has already been confirmed
						Do you need to <a href="{link}">reset your password</a>?
						""".format(link=reset_link)
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
		msg = """Activation link was sent. Check your Email!"""
		if self.request.session.get('language')=='RU':
			msg = """Активация отправлена. Проверь почту!"""
		elif self.request.session.get('language')=='UA':
			msg = """Активація відправлена. Перевір пошту!"""
		request = self.request
		messages.success(request, msg)
		email=form.cleaned_data.get("email")
		obj = EmailActivation.objects.email_exists(email).first()
		user = obj.user
		new_activation = EmailActivation.objects.create(user=user, email=email)
		new_activation.send_activation(request.session.get('language'))
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

	def get_context_data(self, *args, **kwargs):
		context = super(RegisterLoginView, self).get_context_data(*args,**kwargs)
		if self.request.session.get('language') == 'RU':
			context['title'] = 'Войти | Зарегистрироваться'
			context['or_option'] = 'Или'
			context['password_forgot'] = 'Забыл_а пароль?'
		elif self.request.session.get('language') == 'UA':
			context['title'] = 'Увійти | Зареєструватися'
			context['or_option'] = 'Або'
			context['password_forgot'] = 'Забув/забула пароль?'
		else:
			context['title'] = 'Login | Register'
			context['or_option'] = 'Or'
			context['password_forgot'] = 'Forgot password?'
		return context

	def form_valid(self, form):
		next_path = self.get_next_url()
		user = authenticate(form.request, username=form.cleaned_data.get('email'), password=form.cleaned_data.get('password'))
		user_objects = User.objects.filter(email=form.cleaned_data.get('email')).exists()
		link_sent2 = EmailActivation.objects.email_exists(form.cleaned_data.get('email')).exists()
		if user_objects is False:
			form.save()
			user_created = User.objects.filter(email=form.cleaned_data.get('email')).first()
			LanguagePreference.objects.create(user=user_created, language=self.request.session.get('language'))
			next_path = 'login'
			if self.request.session.get('language') == 'RU':
				msg1 = "Пожалуйста, проверь свою почту, чтобы подтвердить аккаунт. " + form.cleaned_data.get('msg')
			elif self.request.session.get('language') == 'UA':
				msg1 = "Будь ласка, перевір свою пошту, щоб підтвердити аккаунт. " + form.cleaned_data.get('msg')
			else:
				msg1 = "Please check your email to confirm your account. " + form.cleaned_data.get('msg')
			messages.add_message(form.request, messages.SUCCESS, mark_safe(msg1))
			return redirect(next_path)
		elif link_sent2:
			if self.request.session.get('language') == 'RU':
				msg2 = "Мейл не подтвержден. " + form.cleaned_data.get('msg')
			elif self.request.session.get('language') == 'UA':
				msg2 = "Мейл не підтверджений. " + form.cleaned_data.get('msg')
			else:
				msg2 = "Email not confirmed. " + form.cleaned_data.get('msg')
			messages.add_message(form.request, messages.WARNING, mark_safe(msg2))
		elif user is None:
			next_path = 'login'
			if self.request.session.get('language') == 'RU':
				msg3 = "Неверный пароль. Попробуй еще раз!"
			elif self.request.session.get('language') == 'UA':
				msg3 = "Невірний пароль. Спробуй ще раз!"
			else:
				msg3 = "The password seems to be wrong. Try again!"
			messages.add_message(form.request, messages.WARNING, mark_safe(msg3))
			return redirect(next_path)
		else:
			language_pref_login_page = self.request.session.get('language')
			login(form.request, user)
			language_pref = LanguagePreference.objects.filter(user=user)
			if language_pref.exists():
				self.request.session['language'] = language_pref.first().language.upper()
			else:
				self.request.session['language'] = language_pref_login_page.upper()
				LanguagePreference.objects.create(user=user, language=language_pref_login_page.lower())
			if self.request.session.get('language') == 'RU':
				messages.add_message(form.request, messages.SUCCESS, 'Ты на сайте')
			elif self.request.session.get('language') == 'UA':
				messages.add_message(form.request, messages.SUCCESS, 'Ти на сайті')
			else:
				messages.add_message(form.request, messages.SUCCESS, "You're in")				
		return redirect(next_path)

def add_message(backend, user, request, response, *args, **kwargs):
	if request.session.get('language') == 'RU':
		messages.add_message(request, messages.SUCCESS, 'Ты на сайте')
	elif request.session.get('language') == 'UA':
		messages.add_message(request, messages.SUCCESS, 'Ти на сайті')
	else:
		messages.add_message(request, messages.SUCCESS, "You're in")

class UserDetailUpdateView(LoginRequiredMixin, RequestFormAttachMixin, UpdateView):
	form_class = UserDetailChangeForm
	template_name='accounts/detail-update-view.html'
	def get_object(self):
		return self.request.user

	def get_context_data(self, *args, **kwargs):
		context = super(UserDetailUpdateView, self).get_context_data(*args,**kwargs)
		if self.request.session.get('language') == 'RU':
			context['title'] = 'Обновить аккаунт'
			context['password_btn'] = 'Изменить пароль'
			context['save_btn'] = 'Сохранить'
			context['logout_btn'] = 'Выйти'
		elif self.request.session.get('language') == 'UA':
			context['title'] = 'Оновити аккаунт'
			context['password_btn'] = 'Змінити пароль'
			context['save_btn'] = 'Зберегти'
			context['logout_btn'] = 'Выйти'
		else:
			context['title'] = 'Update your details'
			context['password_btn'] = 'Change password'
			context['save_btn'] = 'Save'
			context['logout_btn'] = 'Logout'
		return context

	def get_success_url(self):
		return reverse("accounts:user-update")

class ProfileView(DetailView):
	template_name = 'accounts/profile.html'

	def get_context_data(self, *args, **kwargs):
		username = self.kwargs.get('username')
		user  = User.objects.filter_by_username(username=username)
		context = super(ProfileView, self).get_context_data(*args,**kwargs)
		context['products'] = Product.objects.filter(user=user).authentic()
		if self.request.session.get('language') == 'RU':
			context['btn_title'] = 'Написать'
			context['items_title'] = 'Айтемы:'
			context['no_items'] = 'Пока что здесь пусто'
		elif self.request.session.get('language') == 'UA':
			context['btn_title'] = 'Написати'
			context['items_title'] = 'Айтеми:'
			context['no_items'] = 'Поки що тут пусто'
		else:
			context['btn_title'] = 'Message'
			context['items_title'] = 'Items:'
			context['no_items'] = 'No items yet'
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
		print(wished_products)
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
		if self.request.session.get('language') == 'RU':
			context={
			'title':'Избранное:',
			'emptiness':'Пока что здесь пусто',
			'wishes':wished_products
			}
		elif self.request.session.get('language') == 'UA':
			context={
			'title':'Улюблене:',
			'emptiness':'Пока що тут пусто',
			'wishes':wished_products
			}
		else: 
			context={
			'title':'Wishlist:',
			'emptiness':'No items yet',
			'wishes':wished_products
			}
		return context
	# 	user = self.request.user
	# 	all_wishes = user.wishes_user.all()
	# 	wished_products = [wish.product for wish in all_wishes]
	# 	context['wishes'] = wished_products
	# 	return context

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








