from django import forms
from django.utils.translation import gettext as _





class ContactForm(forms.Form):
	email = forms.EmailField(widget=forms.EmailInput(attrs={
		'class':'form-control',
		'placeholder':_('Your Email')


		}))
	content = forms.CharField(widget=forms.Textarea(attrs={
		'class':'form-control',
		'placeholder':_('Your message'),
		}),label=_('Content'))
	def __init__(self, request, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		self.request = request
		self.fields['email'].initial = request.user.email
		self.fields['email'].widget.attrs['readonly'] = True
