from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.core.urlresolvers import reverse
from accounts.models import GuestEmail
import stripe
from django.core.validators import RegexValidator




STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_1l8zkhQ1TSie6osuv340q2gy00sykrXaRe")
STRIPE_PUB_KEY =  getattr(settings, "STRIPE_PUB_KEY", 'pk_test_QZ1Bl6pNnSFwcWXaPOFaC2dx009AMrZvdk')
User=settings.AUTH_USER_MODEL



# class Rating(models.Model):
# 	rating = models.DecimalField(decimal_places=1, max_digits=2, default=0)
# 	points = models.DecimalField(decimal_places=1, max_digits=2, default=0)
# 	users  = models.IntegerField()
	

# 	def __str__(self):
# 		return self.billing_profile
# 	def calculate_rating(self):
# 		points = self.points
# 		users = self.users
# 		rating = round((point/users),1)
# 		self.rating = rating
# 		self.save()


class BillingProfileManager(models.Manager):
	def new_or_get(self, request):
		user=request.user
		guest_email_id = request.session.get('guest_email_id')
		created=False
		obj=None
		if user.is_authenticated():
			obj, created = self.model.objects.get_or_create(
														user=user, email=user.email)
		elif guest_email_id is not None:
			email_obj = GuestEmail.objects.get(id=guest_email_id)
			obj, created = self.model.objects.get_or_create(
														email=email_obj.email)
		else: 
			pass
		return obj, created

class BillingProfile(models.Model):
	user        = models.OneToOneField(User, null=True, blank=True, related_name='billing_profile')
	email       = models.EmailField()
	active      = models.BooleanField(default=True)
	timestamp   = models.DateTimeField(auto_now_add=True)
	update      = models.DateTimeField(auto_now=True)
	customer_id = models.CharField(max_length=120, null=True, blank=True)
	rating      = models.DecimalField(decimal_places=1, max_digits=16, default=0, null=True)
	objects     = BillingProfileManager()
	def __str__(self):
		return self.email

	def charge(self, order_obj, card=None):
		return Charge.objects.do(self, order_obj, card)

	def get_cards(self):
		return self.card_set.all()

	def get_payment_method_url(self):
		return reverse('billing-payment-method')

	@property
	def has_card(self): # instance.has_card
		card_qs = self.get_cards()
		return card_qs.exists() # True or False

	@property
	def default_card(self):
		default_cards = self.get_cards().filter(active=True, default=True)
		if default_cards.exists():
			return default_cards.first()
		return None

	def count_feedbacks(self):
		feedbacks = Feedback.objects.filter(to_user=self)
		return feedbacks.count()

	def set_cards_inactive(self):
		cards_qs = self.get_cards()
		cards_qs.update(active=False)
		return cards_qs.filter(active=True).count()

	def refresh_rating(self):
		rating_arr = Feedback.objects.values_list('rating', flat=True)
		rating_sum = sum(rating_arr)
		self.rating = rating_sum
		self.save()

	@property
	def calculated_rating(self):
		rating_points = self.rating
		feedbacks = self.count_feedbacks()
		calculated_rating = round((rating_points/feedbacks),1)
		return calculated_rating



def billing_profile_created_reciever(sender, instance, created, *args, **kwargs):
	if created:
		billing_profile = instance
		card = Card.objects.new_or_get(billing_profile=billing_profile)
	# if not instance.customer_id and instance.email:
	# 	# print("API REQUEST")
	# 	customer = stripe.Customer.create(email = instance.email)
	# 	# print(customer)
	# 	instance.customer_id = customer.id
post_save.connect(billing_profile_created_reciever, sender=BillingProfile)

def user_created_reciever(sender, instance, created, *args, **kwargs):
	if created and instance.email:
		BillingProfile.objects.get_or_create(user=instance, email=instance.email)
post_save.connect(user_created_reciever, sender=User)


class Feedback(models.Model):
	from_user = models.OneToOneField(User, null=True, blank=False, related_name='feedback')
	to_user   = models.OneToOneField(BillingProfile, null=True, blank=False, related_name='feedback')
	rating    = models.DecimalField(decimal_places=1, max_digits=2, default=0, blank=False, null=True)
	comment   = models.TextField(default='', blank=True)

	def __str__(self):
		return self.to_user.email

def feedback_created_reciever(sender, instance, created, *args, **kwargs):
	if created:
		to_user = instance.to_user
		to_user.refresh_rating()

post_save.connect(feedback_created_reciever, sender=Feedback)



class CardManager(models.Manager):
	def new_or_get(self, billing_profile):
		billing_profile=billing_profile
		created=False
		obj=None
		obj, created = self.model.objects.get_or_create(
														billing_profile=billing_profile)
		return obj, created
class Card(models.Model):
	billing_profile = models.ForeignKey(BillingProfile, related_name='card')
	holder          = models.CharField(max_length=50, null=True, blank=True)
	number          = models.CharField(max_length=16, null=True, blank=True, validators=[RegexValidator(r'^\d+$')])
	month           = models.CharField(max_length=2, null=True, blank=True, validators=[RegexValidator(r'^\d+$')])
	year            = models.CharField(max_length=2, null=True, blank=True, validators=[RegexValidator(r'^\d+$')])
	cvv             = models.CharField(max_length=3, null=True, blank=True, validators=[RegexValidator(r'^\d+$')])
	timestamp       = models.DateTimeField(auto_now_add=True)
	card_token      = models.TextField(null=True, blank=True)
	active          = models.BooleanField(default=True)
	default         = models.BooleanField(default=True)
	objects         = CardManager()
	def __str__(self):
		return "{} {} {}".format(self.billing_profile, self.number, self.holder)

	def is_valid_card(self):
		valid = True
		if self.number is None or self.holder is None:
			return False
		if self.holder == '' or self.number == '':
			return False 
		if self.number is not None:
			if len(str(self.number)) != 16:
				return False
		return valid

class ChargeManager(models.Manager):
	def do(self, billing_profile, order_obj, card=None): # Charge.objects.do()
		card_obj = card
		if card_obj is None:
			cards = billing_profile.card_set.filter(default=True) # card_obj.billing_profile
			if cards.exists():
				card_obj = cards.first()
		if card_obj is None:
			return False, "No cards available"
		c = stripe.Charge.create(
			  amount = int(order_obj.total * 100), # 39.19 --> 3919
			  currency = "usd",
			  customer =  billing_profile.customer_id,
			  source = card_obj.stripe_id,
			  metadata={"order_id":order_obj.order_id},
			)
		new_charge_obj = self.model(
				billing_profile = billing_profile,
				stripe_id = c.id,
				paid = c.paid,
				refunded = c.refunded,
				outcome = c.outcome,
				outcome_type = c.outcome['type'],
				seller_message = c.outcome.get('seller_message'),
				risk_level = c.outcome.get('risk_level'),
		)
		new_charge_obj.save()
		return new_charge_obj.paid, new_charge_obj.seller_message

class Charge(models.Model):
	billing_profile         = models.ForeignKey(BillingProfile)
	stripe_id               = models.CharField(max_length=120)
	paid                    = models.BooleanField(default=False)
	refunded                = models.BooleanField(default=False)
	outcome                 = models.TextField(null=True, blank=True)
	outcome_type            = models.CharField(max_length=120, null=True, blank=True)
	seller_message          = models.CharField(max_length=120, null=True, blank=True)
	risk_level              = models.CharField(max_length=120, null=True, blank=True)

	objects = ChargeManager()


# ---------------------------------------------------------------

# FOR UPDATING A DEFAULT CARD
# def new_card_post_save_receiver(sender, instance, created, *args, **kwargs):
#     if instance.default:
#         billing_profile = instance.billing_profile
#         qs = Card.objects.filter(billing_profile=billing_profile).exclude(pk=instance.pk)
#         qs.update(default=False)
# post_save.connect(new_card_post_save_receiver, sender=Card)


#FOR STRIPE CARD
# class CardManager(models.Manager):
# 	def all(self, *args, **kwargs): # ModelKlass.objects.all() --> ModelKlass.objects.filter(active=True)
# 		return self.get_queryset().filter(active=True)
# 	def add_new(self, billing_profile, token):
# 		if token:
# 			customer = stripe.Customer.retrieve(billing_profile.customer_id)
# 			stripe_card_response = customer.sources.create(source=token)
# 			new_card = self.model(
# 				billing_profile=billing_profile,
# 				stripe_id = stripe_card_response.id,
# 				brand = stripe_card_response.brand,
# 				country = stripe_card_response.country,
# 				exp_month = stripe_card_response.exp_month,
# 				exp_year = stripe_card_response.exp_year,
# 				last4 = stripe_card_response.last4
# 				)
# 			new_card.save()
# 			return new_card
# 		return None

# class Card(models.Model):
# 	billing_profile         = models.ForeignKey(BillingProfile)
# 	stripe_id               = models.CharField(max_length=120)
# 	brand                   = models.CharField(max_length=120, null=True, blank=True)
# 	country                 = models.CharField(max_length=20, null=True, blank=True)
# 	exp_month               = models.IntegerField(null=True, blank=True)
# 	exp_year                = models.IntegerField(null=True, blank=True)
# 	last4                   = models.CharField(max_length=4, null=True, blank=True)
# 	default                 = models.BooleanField(default=True)
# 	active                  = models.BooleanField(default=True)
# 	timestamp               = models.DateTimeField(auto_now_add=True)
# objects = CardManager()