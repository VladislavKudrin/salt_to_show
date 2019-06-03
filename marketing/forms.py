from django import forms

from .models import MarketingPreference


class MarketingPreferenceForm(forms.ModelForm):
	subscribed = forms.BooleanField(label = 'Recieve marketing email?', required=False)
	class Meta:
		model = MarketingPreference
		fields = [
			'subscribed',



		]