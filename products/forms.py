from django.http import JsonResponse
from django import forms
from django.contrib import messages
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.core.validators import validate_image_file_extension


from .models import Product, ImageOrderUtil, ProductImage
from categories.models import Size, Brand

from ecommerce.utils import random_string_generator
from image_uploader.models import UploadedFile
from image_uploader.validators import validate_file_extension

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
	image = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, 'class':'image-upload-button','accept':'image/*','id':'image_custom'} ))
	def clean_image(self):
		form_id = self.request.POST.get('form_id')
		cleaned_images = UploadedFile.objects.filter(form_id=form_id)
		if len(cleaned_images)>8:
			raise forms.ValidationError("Too many files, should be 8")
		return cleaned_images
		
	def save(self, commit=True):
		product = super(ProductCreateForm, self).save(commit=False)
		product.user = self.request.user
		product.active = True
		form_id = self.request.POST.get('form_id')
		if commit:
			product.save()
			images = self.cleaned_data['image']
			for idx, file in enumerate(images):
				ProductImage.objects.create(
					product=product,
					image=file.uploaded_file.file,
					slug=product.slug,
					image_order=idx+1
									)
			UploadedFile.objects.delete_uploaded_files(form_id)
		return product
		
class UploadFileForm(forms.Form):
	image = forms.FileField()






class ProductUpdateForm(ProductCreateForm):
	def __init__(self, request, slug=None, *args, **kwargs):
		super(ProductUpdateForm, self).__init__(request, *args, **kwargs)
		product = Product.objects.get(slug=slug)
		category = product.category
		size = Size.objects.filter(size_for__icontains=category)
		self.fields['size'].queryset = size
		brand = Brand.objects.get(id=self.initial['brand'])
		self.initial['brand']=brand.brand_name
















