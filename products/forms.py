from django.http import JsonResponse
from django import forms
from django.contrib import messages
from PIL import Image
from django_file_form.forms import MultipleUploadedFileField, FileFormMixin
from django_file_form.models import UploadedFile

from .models import Product, Image, ImageOrderUtil
from categories.models import Size, Brand

from ecommerce.utils import random_string_generator



class ProductCreateForm(forms.ModelForm):
	brand = forms.CharField(label='Brand', required=True, widget=forms.TextInput(attrs={"class":'form-control brandautofill',  "placeholder":'Enter a Brand'}))
	class Meta:
		model = Product
		fields = [
		'title',
		'description',
		'price',
		'brand',
		'sex',
		'category',
		'size',
			]
	def __init__(self, request, *args, **kwargs):#
		super(ProductCreateForm, self).__init__(*args, **kwargs)
		self.request = request
	

	def clean_category(self):
		request = self.request
		data = self.cleaned_data
		if data.get('category') == 'select a category':
			self.add_error('category', 'Please, select a category')
		return data.get('category')

	def clean_brand(self):
		data = self.cleaned_data
		brands = Brand.objects.all()
		brand_cleaned = data.get('brand')
		brand_instance = brands.filter(brand_name=brand_cleaned)
		if brand_instance.exists():
			instance=brand_instance.first()
			return instance
		else:
			self.add_error('brand', 'Please, select existing brand')



class ImageForm(ProductCreateForm):
	image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'class':'image-upload-button'} ))
	def clean_image(self):
		print(self.cleaned_data)
	# image = MultipleUploadedFileField()
	# def clean_image(self):
	# 	data = self.cleaned_data
	# 	image = data.get('image')
	# 	if len(image)>8:
	# 		raise forms.ValidationError("Too many files, should be 8")
	# 	for img in image:
	# 		img_ = str(img)
	# 		filename, ext = img_.rsplit('.', 1)
	# 		allowed_ext = {'jpg', 'JPG', 'JPEG', 'jpeg'}
	# 		if ext not in allowed_ext: 
	# 			# messages.add_message(self.request, messages.ERROR, 'Allowed extentions are ".jpg, .jpeg"')
	# 			raise forms.ValidationError('Not a valid extension')
	# 	return image

	def save(self, commit=True):
		product = super(ProductCreateForm, self).save(commit=False)
		product.user = self.request.user
		product.active = True
		if commit:
			product.save()
		# for idx, file in enumerate(self.cleaned_data['image']):
		# 	print(file.form_id)
		# 	print(file)
		# 	Image.objects.create(
		# 		product=product,
		# 		image=file,
		# 		slug=product.slug,
		# 		image_order=idx+1
		# 						)
		# self.delete_temporary_files()
		return product
		


class ProductUpdateForm(ProductCreateForm):
	def __init__(self, request, slug=None, *args, **kwargs):
		super(ProductUpdateForm, self).__init__(request, *args, **kwargs)
		product = Product.objects.get(slug=slug)
		category = product.category
		size = Size.objects.filter(size_for__icontains=category)
		self.fields['size'].queryset = size
		brand = Brand.objects.get(id=self.initial['brand'])
		self.initial['brand']=brand.brand_name
















