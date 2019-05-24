from django.http import JsonResponse
from django import forms
from django_file_form.forms import MultipleUploadedFileField, FileFormMixin
from .models import Product, Image

class ProductCreateForm(FileFormMixin, forms.ModelForm):
	class Meta:
		model = Product
		fields = [
		'title',
		'description',
		'price',
		'sex',
		'category',
		'size',
			]
	def __init__(self, request, *args, **kwargs):
		self.request = request
		super(ProductCreateForm, self).__init__(*args, **kwargs)	

	def clean_category(self):
		request = self.request
		data = self.cleaned_data
		if data.get('category') == 'select a category':
			self.add_error('category', 'Please, select a category')
		return data.get('category')

	# def save(self, commit=True):
	# 	product = super(ProductCreateForm, self).save(commit=False)
	# 	product.user = self.request.user
	# 	product.active = True
	# 	if commit:
	# 		product.save()
	# 	return product







class ImageForm(ProductCreateForm):
	image = MultipleUploadedFileField()
	def save(self, commit=True):
		product = super(ProductCreateForm, self).save(commit=False)
		product.user = self.request.user
		product.active = True
		if commit:
			product.save()
		for file in self.cleaned_data['image']:
			Image.objects.create(
				product=product,
				image=file
								)
		self.delete_temporary_files()
		return product
		



