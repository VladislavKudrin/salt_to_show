from django import forms
from .models import Card
from .models import BillingProfile

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

    def save(self, commit=True):
        print(self.cleaned_data)