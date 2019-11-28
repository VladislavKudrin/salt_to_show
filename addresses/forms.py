from django import forms

from .models import Address

from billing.models import BillingProfile
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'name',
            'additional_line',
            'street',
            'number',
            'postal_code',
            'city',
            'state',
            'country',
            'post_office'        
        ]

    def __init__(self, request, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.request=request



class AddressCheckoutForm(forms.ModelForm):
    """
    User-related checkout address create form
    """
    class Meta:
        model = Address
        fields = [
            'name',
            'additional_line',
            'street',
            'number',
            'postal_code',
            'city',
            'state',
            'country',
            'post_office'        
        ]
