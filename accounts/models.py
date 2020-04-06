from datetime import timedelta
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
import random
import os
from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils import timezone
from django.utils.translation import gettext as _ 
from ecommerce.utils import unique_key_generator, random_string_generator_username
from products.models import Product

DEFAULT_ACTIVATION_DAYS = getattr(settings, "DEFAULT_ACTIVATION_DAYS", 7)

LANGUAGE_CHOISES = (
	('ru', 'RU'),
	('ua', 'UA'),
	('en', 'EN')
	)

def get_filename_ext(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext

def upload_image_path(instance, filename):
	new_filename = random.randint(1,31231231)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
	return "profile_fotos/{new_filename}/{final_filename}".format(
		new_filename=new_filename,
		final_filename=final_filename)
	
class UserManager(BaseUserManager):
	error_css_class = 'error'
	def check_username(self, username):
		user = self.filter(username=username)
		if user.exists(): 
			username_new = str(username) + random_string_generator_username()
			return username_new
		return username


	def filter_by_username(self, username):
		user_email_obj = self.filter(username=username).first()
		user_obj = self.get_by_natural_key(username=user_email_obj)
		return user_obj
	


	def create_user(self, email, username=None, full_name = None, password=None, is_active=True, is_staff=False, is_admin=False):
		if not email:
			raise ValueError("Users must have an email address and username!")
		# if not password:
		# 	raise ValueError("Users must have a password!")
		user_obj = self.model(
				email = self.normalize_email(email),
				username = username,
				full_name = full_name,
			)

		user_obj.set_password(password)
		user_obj.staff = is_staff
		user_obj.admin = is_admin
		user_obj.is_active = is_active
		user_obj.save(using=self._db)
		return user_obj

	def create_staffuser(self, email, username=None, full_name=None, password = None):
		user = self.create_user(
				email,
				username,
				full_name,
				password = password,
				is_staff = True
				
			)
		return user

	def create_superuser(self, email, username=None, full_name=None, password = None, is_admin=None, is_active=None):
		username_unchecked = email.split("@")[0]
		username = User.objects.check_username(username_unchecked)
		user = self.create_user(
				email,
				username,
				full_name,
				password = password,
				is_staff = True,
				is_active = True,
				is_admin = True,
			)
		return user

class Region(models.Model):
	region        = models.CharField(max_length=120, blank=True, null=True)
	region_code   = models.CharField(max_length=120, blank=True, null=True)
	currency      = models.CharField(max_length=120, default='USD', blank=True, null=True)
	currency_mult = models.DecimalField(decimal_places=6, max_digits=10, default=0, null=True)
	def __str__(self):
		return str(self.region)

class User(AbstractBaseUser):
	username     = models.CharField(max_length=255, blank=False, null=True, unique=True)
	email        = models.EmailField(max_length=255, unique=True)
	full_name    = models.CharField(max_length=255, blank=True, null=True)
	is_active    = models.BooleanField(default=True)
	staff        = models.BooleanField(default=False)
	admin        = models.BooleanField(default=False)
	timestamp    = models.DateTimeField(auto_now_add=True)
	profile_foto = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
	wishes       = models.ManyToManyField(Product, related_name='users', blank=True)
	region       = models.ForeignKey(Region, related_name='users_region', blank=True, null=True)
	bio 		 = models.TextField(blank=True, null=True, max_length=155) # like in insta
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []#additional required field
	objects=UserManager()

	def __str__(self):
		return self.email

	def get_absolute_url(self):
		return reverse('accounts:profile', kwargs={"username":self.username})

	def get_full_name(self):
		if self.full_name:
			return self.full_name
		return self.email

	def get_short_name(self):
		return self.email

	def has_perm(self, perm, obj = None):
		return True

	def has_module_perms(self, app_label):
		return True

	def get_wishes(self):
		if self.wishes:
			return self.wishes
		pass
	@property
	def is_staff(self):
		return self.staff

	@property
	def is_admin(self):
		return self.admin

class LanguagePreference(models.Model):
	user     = models.ForeignKey(User, related_name='language')
	language = models.CharField(max_length=120, default='en', choices=LANGUAGE_CHOISES)
	def __str__(self):
		return str(self.user)

class WishlistQuerySet(models.query.QuerySet):
	def available(self):
		return self.exclude(product__order__status='paid')

class WishlistManager(models.Manager):
	def get_queryset(self):
		return WishlistQuerySet(self.model, using=self._db)

	def available(self):
		return self.get_queryset().available()

class Wishlist(models.Model):
	user      = models.ForeignKey(User, related_name='wishes_user')
	product   = models.ForeignKey(Product, related_name='wishes_products')
	timestamp = models.DateTimeField(auto_now_add=True)


	objects = WishlistManager()

class EmailActivationQuerySet(models.query.QuerySet):
	def confirmable(self):
		now = timezone.now()
		start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)

		end_range = now
		#activated = False
		#forced_expired = False
		return self.filter(
					activated = False,
					forced_expired = False
		).filter(
			timestamp__gt=start_range,  #greater than
			timestamp__lte=end_range  #less than
		)

class EmailActivationManager(models.Manager):
	def get_queryset(self):
		return EmailActivationQuerySet(self.model, using=self._db)

	def confirmable(self):
		return self.get_queryset().confirmable()

	def email_exists(self, email):
		return self.get_queryset().filter(
				 Q(email=email) 
				|Q(user__email=email)
			).filter(
				activated=False
			)

	def confirmed_activation_exists(self, email):
		return self.get_queryset().filter(
				 Q(email=email) 
				|Q(user__email=email)
			).filter(
				activated=True
			)
	
class EmailActivation(models.Model):
	user            = models.ForeignKey(User)
	email           = models.EmailField()
	key             = models.CharField(max_length=120, blank=True,null=True)
	activated       = models.BooleanField(default=False)
	forced_expired  = models.BooleanField(default=False)
	expires         = models.IntegerField(default=7)#Days
	timestamp       = models.DateTimeField(auto_now_add = True)
	update          = models.DateTimeField(auto_now = True)

	error_css_class = 'error'
	objects = EmailActivationManager()
	def __str__(self):
		return self.email

	def can_activate(self):
		qs=EmailActivation.objects.filter(pk=self.pk).confirmable()
		if qs.exists():
			return True
		return False

	def activate(self):
		if self.can_activate():
			user=self.user
			user.is_active=True
			user.save()
			self.activated=True
			self.save()
			return True
		return False

	def regenerate(self):
		self.key=None
		self.save()
		if self.key is not None:
			return True
		return False

	def send_activation(self):
		if not self.activated and not self.forced_expired:
			if self.key:
				base_url = getattr(settings, 'BASE_URL', 'https://www.saltysalt.co')
				key_path = reverse("accounts:email-activate", kwargs={'key':self.key}) #use reverse
				path = "{base}{path}".format(base=base_url, path=key_path)
				context = {
						'path':path,
						'email':self.email

				}
				txt_ = get_template("registration/emails/verify.txt").render(context)
				html_ = get_template("registration/emails/verify.html").render(context)
				subject = _('1-Click Account Verification')
				from_email = settings.DEFAULT_FROM_EMAIL
				recipient_list = [self.email]
				sent_mail=send_mail(
					subject,
					txt_,
					from_email,
					recipient_list,
					html_message=html_,
					fail_silently=False, 
					)
				return sent_mail
			return False

def pre_save_email_activation(sender, instance, *args, **kwargs):
	if not instance.activated and not instance.forced_expired:
		if not instance.key:
			instance.key = unique_key_generator(instance)
pre_save.connect(pre_save_email_activation, sender=EmailActivation)
	
def post_save_language_pref(sender, instance, created, *args, **kwargs):
	if created:
		is_social = instance.user.social_auth.exists()
		is_admin = instance.user.admin
		if not is_social:
			if not is_admin:		
				obj = EmailActivation.objects.create(user=instance.user, email=instance.user.email)
				obj.send_activation()
			else:
				EmailActivation.objects.create(user=instance.user, email=instance.user.email, activated=True)
post_save.connect(post_save_language_pref, sender=LanguagePreference)


		