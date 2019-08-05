from django import forms

class TranslateForm(forms.Form):
	email = forms.EmailField(widget=forms.EmailInput(attrs={
		'class':'form-control',
		'placeholder':'Your Email'
		}))