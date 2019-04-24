from django import forms

from .models import Address

class AddressForm(forms.ModelForm):   #использует форму, которую мы видим в админе
	class Meta:
		model = Address
		fields=[
			#'billing_profile',
			#'adress_type',
			'address_line_1',
			'address_line_2',
			'city',
			'state',
			'country',
			'postal_code'
			]


