from django import forms
from .models import Card
from .models import BillingProfile
from django.utils.translation import gettext as _ 

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = [
            'holder',
            'number',
            'month',
            'number',
            'year', 
            'cvv',      
        ]

    def __init__(self, request, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        self.request=request
    # def clean_number(self):
    #     number = self.cleaned_data.get('number')
    #     if len(str(number)) != 16:
    #         print('smaller')
    #         msg = ("""This email does not exist or already acivated. Would you like to <a href=""")
    #         raise forms.ValidationError((msg))
    #     return number

    # 