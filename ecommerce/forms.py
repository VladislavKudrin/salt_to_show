from django import forms





class ContactForm(forms.Form):
	email = forms.EmailField(widget=forms.EmailInput(attrs={
		'class':'form-control',
		'placeholder':'Your Email'

		}))
	content = forms.CharField(widget=forms.Textarea(attrs={
		'class':'form-control',
		'placeholder':'Your message'
		}))
	def __init__(self, request, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		self.request = request
		self.lan = request.session.get('language')
		self.fields['email'].initial = request.user.email
		self.fields['email'].widget.attrs['readonly'] = True
		if self.lan == 'RU':
			self.fields['content'].label = "Содержание"
			self.fields['content'].widget.attrs['placeholder'] = 'Твой месседж'
		elif self.lan == 'UA':
			self.fields['content'].label = "Зміст"
			self.fields['content'].widget.attrs['placeholder'] = 'Твій месседж'

	# def clean_email(self):
	# 	email = self.cleaned_data.get('email')
	# 	if not "gmail.com" in email:
	# 		raise forms.ValidationError("Email has to be gmail.com")
	# 	return email

	# def clean_content(self):
	# 	raise forms.ValidationError("Content is wrong")
