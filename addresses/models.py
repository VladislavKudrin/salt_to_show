from django.db import models
from django.core.urlresolvers import reverse
from billing.models import BillingProfile
from ecommerce.utils import alphaSpaces, phone_regex
from django.core.validators import MinLengthValidator


class AddressManager(models.Manager):
	def new_or_get(self, billing_profile):
		billing_profile=billing_profile
		created=False
		obj=None
		obj, created = self.model.objects.get_or_create(
														billing_profile=billing_profile)
		return obj, created
class Address(models.Model):
	billing_profile = models.ForeignKey(BillingProfile, related_name='address')
	name            = models.CharField(max_length=120, null=True, blank=True, validators=[alphaSpaces, MinLengthValidator(6)])
	post_office     = models.CharField(max_length=120, null=True, blank=True)
	phone           = models.CharField(max_length=17, null=True, blank=True, validators=[phone_regex])
	additional_line = models.CharField(max_length=120, null=True, blank=True)
	street          = models.CharField(max_length=120, null=True, blank=True)
	number          = models.CharField(max_length=120, null=True, blank=True)
	postal_code     = models.CharField(max_length=120, null=True, blank=True)
	city            = models.CharField(max_length=120, null=True, blank=True)
	state           = models.CharField(max_length=120, null=True, blank=True)
	country         = models.CharField(max_length=120, null=True, blank=True)
	objects         = AddressManager()

	def __str__(self):
		return str(self.billing_profile) or ' '

	def get_absolute_url(self):
		return reverse("address-update", kwargs={"pk": self.pk})

	def get_short_address(self):
		return "{name} {street}, {city}".format(
			name = self.name or "",
			street = self.street or "",
			city = self.city or ""
		) 

	def get_address(self):
		return "{name}\n{additional_line}\n{street}\n{number}\n{postal_code}\n{city}\n{state}\n{country}\n{post_office}\n{phone}".format(
			name = self.name or "",
			additional_line = self.additional_line or "",
			street = self.street or "",
			number = self.number or "",
			postal_code = self.postal_code or "",
			city= self.city or "",
			state = self.state or "",
			country = self.country or "",
			post_office = self.post_office or "",
			phone = self.phone or ""
			)