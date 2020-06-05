from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template

from ecommerce.utils import unique_key_generator
User = get_user_model()

class User_telegram(models.Model):
	user = models.OneToOneField(User, blank=True, null=True, related_name='user_telegram')
	chat_id = models.CharField(max_length=200,unique=True)
	in_answer_mode = models.BooleanField(blank=False, default=False)
	def __str__(self):
		return self.chat_id
	@property
	def is_logged_in(self):
		try:
			self.user
			if self.user is not None:
				return True
			else:
				return False
		except:
			return False

	def exit_all_modes(self):
		#enter all modes
		LoginMode.objects.filter(user_telegram=self).delete()
		PayMode.objects.filter(user_telegram=self).delete()
		#enter all modes
		self.in_answer_mode=False
		self.save()

	def get_mode(self):
		if self.in_answer_mode:
			#modes
			login_mode = LoginMode.objects.filter(user_telegram=self).exists()
			pay_mode = PayMode.objects.filter(user_telegram=self).exists()
			#modes
			if login_mode:
				return 'login'
			if pay_mode:
				return 'pay'
		else:
			return None

	def get_billing_profile(self):
		try:
			self.user
			if self.user is not None:
				return self.user.billing_profile
			else:
				return None
		except:
			return None



class LoginMode(models.Model):
	user_telegram = models.OneToOneField(User_telegram, related_name='login_mode')
	email         = models.EmailField(max_length=255, blank=True)
	password      = models.CharField(max_length=255, blank=True, null=True)
	def __str__(self):
		return self.email

# def login_mode_post_save(sender, created, instance, *args, **kwargs):
# 	if created:
# 		instance.user_telegram.in_answer_mode = True

# post_save.connect(login_mode_post_save, sender=LoginMode)

class PayMode(models.Model):
	user_telegram = models.OneToOneField(User_telegram, related_name='pay_mode', null=True)
	product_slug = models.CharField(max_length=255, blank=True, null=True)
	def __str__(self):
		return self.product_slug


# def pay_mode_post_save(sender, created, instance, *args, **kwargs):
# 	if created:
# 		instance.user_telegram.in_answer_mode = True
# 		instance.user_telegram.sa

# post_save.connect(pay_mode_post_save, sender=PayMode)

class TelegramActivationQuerySet(models.query.QuerySet):
	def confirmable(self):
		now = timezone.now()
		start_range = now - timedelta(minutes=5)
		end_range = now

		return self.filter(
					activated = False,
		).filter(
			timestamp__gt=start_range,  #greater than
			timestamp__lte=end_range  #less than
		)


class TelegramActivationManager(models.Manager):
	def get_queryset(self):
		return TelegramActivationQuerySet(self.model, using=self._db)

	def confirmable(self):
		return self.get_queryset().confirmable()




class TelegramActivation(models.Model):
	chat_id   = models.CharField(max_length=200)
	email     = models.EmailField(max_length=255, blank=True)
	key       = models.CharField(max_length=120, blank=True,null=True)
	timestamp = models.DateTimeField(auto_now_add = True)
	expires   = models.IntegerField(default=5)#Minutes
	activated = models.BooleanField(default=False)


	objects = TelegramActivationManager()

	def __str__(self):
		return self.email

	def can_activate(self):
		qs=TelegramActivation.objects.filter(pk=self.pk).confirmable()
		if qs.exists():
			return True
		return False

	def regenerate(self):
		self.key=None
		self.save()
		if self.key is not None:
			return True
		return False

	def send_activation(self):
		if not self.activated:
			if self.key:
				key = self.key #use reverse
				context = {
						'key':key,

				}
				txt_ = get_template("bot/emails/activate_telegram.txt").render(context)
				html_ = get_template("bot/emails/activate_telegram.html").render(context)
				subject = 'Telegram Verification'
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


def post_save_telegram_activation(sender, created, instance, *args, **kwargs):
	if not instance.key:
		instance.regenerate()
	else:
		if instance.can_activate():
			instance.send_activation()

def pre_save_telegram_activation(sender, instance, *args, **kwargs):
	if not instance.key:
		instance.key = unique_key_generator(instance)



pre_save.connect(pre_save_telegram_activation, sender=TelegramActivation)
post_save.connect(post_save_telegram_activation, sender=TelegramActivation)







