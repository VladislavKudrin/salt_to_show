from django import forms
from .models import Address
from billing.models import BillingProfile
import os
from ecommerce.settings import BASE_DIR
from django.urls import reverse
from django.utils.translation import gettext as _

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

    def get_latest_postoffices_ua(self):
        path = os.path.join(BASE_DIR, "static_my_project", 'post_offices_ua.txt')
        post_offices = []
        with open(path, 'r') as filehandle:
            for line in filehandle:
                line = line[:-1] # remove linebreak which is the last character of the string
                post_offices.append(line)
        return post_offices

    def get_latest_postoffices_ru(self):
        path = os.path.join(BASE_DIR, "static_my_project", 'post_offices_ru.txt')
        post_offices = []
        with open(path, 'r') as filehandle:
            for line in filehandle:
                line = line[:-1] # remove linebreak which is the last character of the string
                post_offices.append(line)
        return post_offices


    def __init__(self, request, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        post_offices = ['Choose Nova Poshta station'] + self.get_latest_postoffices_ua()

        self.request=request
        self.fields['post_office'] = forms.ChoiceField(choices=tuple([(name, name) for name in post_offices]))
        self.fields['name'].widget.attrs['class']='labels-placement'
        self.fields['phone'].widget.attrs['class']='labels-placement'
        self.fields['name'].label = _('Name')
        self.fields['phone'].label = _('Phone')
        if 'checkout' in request.path:
            self.fields['name'].required = True
            self.fields['phone'].required = True
            self.fields['post_office'].required = True
        else:
            self.fields['name'].required = False
            self.fields['phone'].required = False
            self.fields['post_office'].required = False



    def clean_post_office(self):
        data_office = self.cleaned_data.get('post_office')
        error_message = "Пожалуйста, выбери отделение"
        if 'checkout' in self.request.path:
            if data_office is '' or data_office == 'Choose Nova Poshta station':
                self.add_error('post_office', error_message)
        return data_office




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
