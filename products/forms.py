from django import forms

from .models import Product, Image

class ProductCreateForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = [
		'sex',
		'category',
		'title',
		'description',
		'price',
	]

class ImageForm(forms.ModelForm):
	image = forms.ImageField(label='Image', widget=forms.ClearableFileInput(attrs={'multiple': True}))
	class Meta:
		model = Image
		fields = [
			'image'
		]