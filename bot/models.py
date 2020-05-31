from django.db import models
from django.contrib.auth import get_user_model
# from django.db.models.signals import pre_save, post_save

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
	email         = models.EmailField(max_length=255, unique=True, blank=True)
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

