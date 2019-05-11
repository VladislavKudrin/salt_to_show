from django import forms

from .models import Product, Image

class ProductCreateForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = [
		'title',
		'description',
		'price',
		'sex',
		'category',


	]

class ImageForm(forms.ModelForm):
	image = forms.ImageField(label='Image')
	class Meta:
		model = Image
		fields = [
			'image'
		]