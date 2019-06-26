from django.http import JsonResponse
from django import forms
from django.contrib import messages
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.core.validators import validate_image_file_extension
from django.conf import settings

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
	def __init__(self, request, *args, **kwargs):
		super(ProductCreateForm, self).__init__(*args, **kwargs)
		self.request = request
		self.lan = request.session.get('language')
		self.fields['title'].widget.attrs['placeholder'] = 'Enter a Title'
		self.fields['description'].widget.attrs['placeholder'] = 'Enter a description'
		self.fields['price'].widget.attrs['placeholder'] = 'Enter a price'
		self.fields['price'].initial = ''
		if self.lan == 'RU':
			self.fields['title'].label = "Название"
			self.fields['title'].widget.attrs['placeholder'] = 'Введите название'
			self.fields['description'].label = "Описание"
			self.fields['description'].widget.attrs['placeholder'] = 'Введите описание'
			self.fields['price'].label = "Цена"
			self.fields['price'].widget.attrs['placeholder'] = 'Введите цену'
			self.fields['brand'].label = "Бренд"
			self.fields['brand'].widget.attrs['placeholder'] = 'Введите бренд'
			self.fields['sex'].label = "Пол"
			self.fields['sex'].choices = SEX_CHOICES = (
			('man', 'Мужское'),
			('woman', 'Женское'),
			)
			self.fields['category'].label = "Категория"
			self.fields['category'].choices = CATEGORY_CHOICES = (
			('select a category', 'Выберите категорию'),
			('tops', 'Верх'),
			('bottoms', 'Низ'),
			('accessories', 'Аксессуары'),
			('outerwear', 'Верхняя одежда'),
			('footwear', 'Обувь'),
			)
			self.fields['size'].label = "Размер"


		
	

	def clean_category(self):
		request = self.request
		data = self.cleaned_data
		if data.get('category') == 'select a category':
			if self.lan == 'RU':
				self.add_error('category', 'Пожалуйста, выберите категорию')
			else:
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
			if self.lan == 'RU':
				self.add_error('brand', 'Пожалуйста, выберите существующий бренд')
			else:
				self.add_error('brand', 'Please, select existing brand')



class ImageForm(ProductCreateForm):
	image = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, 'class':'image-upload-button','accept':'image/*','id':'image_custom'} ))
	def __init__(self, request, *args, **kwargs):
		super(ImageForm, self).__init__(request, *args, **kwargs)
		self.fields['image'].label = "Image*"
		if request.session.get('language')=='RU':
			self.fields['image'].label = "Фото*"
	
	def clean_image(self):
		form_id = self.request.POST.get('form_id')
		cleaned_images = UploadedFile.objects.filter(form_id=form_id)
		if len(cleaned_images)==0:
			if self.lan == 'RU':
				raise forms.ValidationError("Загрузите фото")
			else:
				raise forms.ValidationError("You should upload an image")	
		if len(cleaned_images)>settings.IMAGES_UPLOAD_LIMIT:
			if self.lan == 'RU':
				raise forms.ValidationError("Слишком много файлов. Максимальное колличество - 8")
			else:
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
















