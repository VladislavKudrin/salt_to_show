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
            'post_office',
            'phone',      
        ]

    def __init__(self, request, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.request=request
        print(self.request.user.region)
        # user = self.request.user
        # user_region = str(user.region)

        # if "USA" in user_region:
        #     self.fields.pop('state')

        # # if str(user.region).contains("USA"):
        # #     print(user.region)

        # # print(user.region)
        # # print(self.fields)
        # # self.fields = ['name']
        # # print(self.fields)



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
    def save(self, commit=True):
        print('WOWA')
