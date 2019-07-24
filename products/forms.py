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
import re

class ProductCreateForm(forms.ModelForm):
	brand = forms.CharField(label='Brand', required=True, widget=forms.TextInput(attrs={"class":'form-control brandautofill',  "placeholder":'Select a brand'}))
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
		'condition',
			]
	def __init__(self, request, *args, **kwargs):
		super(ProductCreateForm, self).__init__(*args, **kwargs)
		self.request = request
		self.lan = request.session.get('language')
		self.fields['title'].widget.attrs['placeholder'] = 'Some keywords about your item'
		self.fields['description'].widget.attrs['placeholder'] = 'Describe your item in details'
		self.fields['price'].widget.attrs['placeholder'] = 'Enter a price in $'
		self.fields['condition'].widget.attrs['placeholder'] = 'Enter a condition'
		self.fields['price'].initial = ''
		self.fields['sex'].label = 'Gender'
		if self.lan == 'RU':
			self.fields['title'].label = "Название"
			self.fields['title'].widget.attrs['placeholder'] = 'Пара слов про айтем'
			self.fields['description'].label = "Описание"
			self.fields['description'].widget.attrs['placeholder'] = 'Подробно опиши айтем'
			self.fields['price'].label = "Цена (в $)"
			self.fields['price'].widget.attrs['placeholder'] = 'Введи цену в $'
			self.fields['brand'].label = "Бренд"
			self.fields['brand'].widget.attrs['placeholder'] = 'Выбери бренд'
			self.fields['sex'].label = "Гендер"
			self.fields['sex'].choices = SEX_CHOICES = (
			('man', 'Мужское'),
			('woman', 'Женское'),
			)
			self.fields['category'].label = "Категория"
			self.fields['category'].choices = CATEGORY_CHOICES = (
			('select a category', 'Выбери подходящую категорию'),
			('tops', 'Верх'),
			('bottoms', 'Низ'),
			('accessories', 'Аксессуары'),
			('outerwear', 'Верхняя одежда'),
			('footwear', 'Обувь'),
			)
			self.fields['size'].label = "Размер"
			self.fields['condition'].label = "Состояние"
			self.fields['condition'].choices = CONDITION_CHOICES = (
			('item condition', 'Выбери состояние айтема'),
			('new with tags', 'Новая вещь с бирками'),
			('gently used', 'Отличное состояние'),
			('used', 'Нормальное состояние'),
			)


		
	

	def clean_category(self):
		request = self.request
		data = self.cleaned_data
		if data.get('category') == 'select a category':
			if self.lan == 'RU':
				self.add_error('category', 'Пожалуйста, выбери категорию')
			else:
				self.add_error('category', 'Please, select a category')
		return data.get('category')

	def clean_condition(self):
		request = self.request
		data = self.cleaned_data
		if data.get('condition') == 'item condition':
			if self.lan == 'RU':
				self.add_error('condition', 'Пожалуйста, выбери состояние')
			else:
				self.add_error('condition', 'Select an item condition')
		return data.get('condition')

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

	def clean_description(self):
		data = self.cleaned_data
		description = data.get('description')
		if description: 
			description = re.sub(r'\n\s*\n','\n',description,re.MULTILINE)
			length = len(description.splitlines())
			chars = len(description)
			if length > 18: 
				lines = int(length) - int(18)
				message = 'Please, make it shorter. # of lines to be removed: {lines}'.format(lines=lines)
				self.add_error('description', message)
			if chars > 600:
				charss = int(chars) - int(600)
				message = 'Please, make it shorter. # of characters to be removed: {charss}'.format(charss=charss)
				self.add_error('description', message)	
		return description


class ImageForm(ProductCreateForm):
	image = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, 'class':'image-upload-button','accept':'image/*','id':'image_custom'} ))
	def __init__(self, request, *args, **kwargs):
		super(ImageForm, self).__init__(request, *args, **kwargs)
		self.fields['image'].label = "Images*"
		if request.session.get('language')=='RU':
			self.fields['image'].label = "Фото*"
	
	def clean_image(self):
		form_id = self.request.POST.get('form_id')
		cleaned_images = UploadedFile.objects.filter(form_id=form_id)
		print(self.request.POST)
		if len(cleaned_images)==0:
			if self.lan == 'RU':
				raise forms.ValidationError("Загрузи как минимум фото")
			else:
				raise forms.ValidationError("Upload at least one image")	
		if len(cleaned_images)>settings.IMAGES_UPLOAD_LIMIT:
			if self.lan == 'RU':
				raise forms.ValidationError("Слишком много файлов. Максимальное колличество - 8")
			else:
				raise forms.ValidationError("Too many files, max. amount 8")	
		return cleaned_images
		
	def save(self, commit=True):
		product = super(ProductCreateForm, self).save(commit=False)
		product.user = self.request.user
		product.active = True
		form_id = self.request.POST.get('form_id')
		if commit:
			product.save()
			images = self.cleaned_data['image']
			array_rotate = self.request.POST.getlist('rotateTimes')
			array_qq_id = self.request.POST.getlist('qq-file-id')
			qs_rotate = {} 
			for idx, i in enumerate(array_qq_id):
				qs_rotate[i] = array_rotate[idx]
			for idx, file in enumerate(images):
				this_rotate = qs_rotate.get(str(idx))
				file = UploadedFile.objects.rotate_image(image = file.uploaded_file.file, rotated_x = this_rotate)
				ProductImage.objects.create(
					product=product,
					image=file,
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
		description = product.description
		size = Size.objects.filter(size_for__icontains=category)
		self.fields['size'].queryset = size
		brand = Brand.objects.get(id=self.initial['brand'])
		self.initial['brand']=brand.brand_name
















