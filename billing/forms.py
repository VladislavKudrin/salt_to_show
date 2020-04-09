from django import forms
from .models import BillingProfile, Card, Feedback
from orders.models import Order
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



class CardModalForm(CardForm):
    def clean_number(self):
        number = self.cleaned_data.get('number')
        if len(str(number)) != 16:
            msg = _("Enter a valid card number")
            raise forms.ValidationError((msg))
        return number

    



RATING_CHOICES = [x * 0.5 for x in range(11)]
class FeedbackForm(forms.ModelForm):
    order_id = forms.CharField(required=False, widget=forms.TextInput(attrs={"style":"display:none"}))
    class Meta:
        model = Feedback
        fields = [
                'rating',
                'comment',
        ]
    def __init__(self, request, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.request=request
        self.fields['comment'].widget.attrs['rows'] = '5'
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating in RATING_CHOICES:
            return rating
        else:
            raise forms.ValidationError('NO')
    def clean_order_id(self):
        order_id = self.cleaned_data.get('order_id')
        order = Order.objects.filter(order_id=order_id)
        if order.exists():
            order = order.first()
            billing_profile, created = BillingProfile.objects.new_or_get(self.request)
            if order.billing_profile == billing_profile:
                return order
        return forms.ValidationError('NO')
    def save(self, commit=True):
        feedback = super(FeedbackForm, self).save(commit=False)
        from_user = self.request.user
        order = self.cleaned_data.get('order_id')
        comment = self.cleaned_data.get('comment')
        to_user = order.product.user.billing_profile
        rating = self.cleaned_data.get('rating')
        feedback.from_user = from_user
        feedback.to_user = to_user
        feedback.comment = comment
        feedback.rating = rating
        if commit:
            feedback.save()
            order.feedback = feedback
            order.save()
        return feedback

















