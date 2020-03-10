from django import forms
from django.utils.translation import gettext as _





class ContactForm(forms.Form):
	email = forms.EmailField(widget=forms.EmailInput(attrs={
		'class':'form-control labels-placement',
		# 'placeholder':_('Your Email')


		}))
	content = forms.CharField(widget=forms.Textarea(attrs={
		'class':'form-control',
		'placeholder':_('Your message'),
		}),label=False)
	def __init__(self, request, order_id=None, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		self.request = request
		self.fields['email'].initial = request.user.email
		self.fields['email'].widget.attrs['readonly'] = True
		if order_id is not None:
			self.fields['content'].initial = _('Order Id: ') + order_id