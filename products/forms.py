from django.http import JsonResponse
from django import forms
from django.contrib import messages
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.core.validators import validate_image_file_extension
from django.conf import settings

from .models import Product, ImageOrderUtil, ProductImage
from categories.models import Size, Brand, Undercategory, Overcategory, Gender, Category, Condition

from ecommerce.utils import random_string_generator
from image_uploader.models import UploadedFile
from image_uploader.validators import validate_file_extension
import re

class ProductCreateForm(forms.ModelForm):
	brand = forms.CharField(label='Brand', required=True, widget=forms.TextInput(attrs={"class":'form-control brandautofill',  "placeholder":'Select a brand'}))
	sex = forms.CharField(label='Gender', required=True, widget=forms.TextInput(attrs={"class":"custom-readonly", "placeholder":'Select a gender'}))
	undercategory = forms.CharField(label='Category', required=True, widget=forms.TextInput(attrs={"class":"custom-readonly", "placeholder":'Select a category'}))
	size = forms.CharField(label='Size', required=True, widget=forms.TextInput(attrs={"class":"custom-readonly", "placeholder":'Select a size'}))
	condition = forms.CharField(label='Condition', required=True, widget=forms.TextInput(attrs={"class":"custom-readonly", "placeholder":'Select a condition'}))
	class Meta:
		model = Product
		fields = [
		'title',
		'description',
		'price',
		'brand',
		'sex',
		'undercategory',
		'size',
		'condition',
			]
	def __init__(self, request, *args, **kwargs):
		super(ProductCreateForm, self).__init__(*args, **kwargs)
		self.request = request
		self.lan = request.session.get('language')
		self.fields['sex'].widget.attrs['readonly'] = True
		self.fields['undercategory'].widget.attrs['readonly'] = True
		self.fields['size'].widget.attrs['readonly'] = True
		self.fields['condition'].widget.attrs['readonly'] = True
		self.fields['title'].widget.attrs['placeholder'] = 'Some keywords about your item'
		self.fields['description'].widget.attrs['placeholder'] = 'Describe your item in details'
		self.fields['price'].widget.attrs['placeholder'] = 'Enter a price in $'
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
			self.fields['sex'].widget.attrs['placeholder'] = 'Выбери гендер'
			self.fields['undercategory'].label = "Категория"
			self.fields['undercategory'].widget.attrs['placeholder'] = 'Выбери категорию'
			self.fields['condition'].widget.attrs['placeholder'] = 'Выбери состояние'
			self.fields['size'].widget.attrs['placeholder'] = 'Выбери размер'
			# self.fields['category'].label = "Категория"
			# self.fields['category'].choices = CATEGORY_CHOICES = (
			# ('select a category', 'Выбери подходящую категорию'),
			# ('tops', 'Верх'),
			# ('bottoms', 'Низ'),
			# ('accessories', 'Аксессуары'),
			# ('outerwear', 'Верхняя одежда'),
			# ('footwear', 'Обувь'),
			# )
			self.fields['size'].label = "Размер"
			self.fields['condition'].label = "Состояние"



		
	def clean_sex(self):
		request = self.request
		data_sex = self.cleaned_data.get('sex')
		print(self.cleaned_data, 'privet')
		sex = Gender.objects.filter(id=int(data_sex))
		self.cleaned_data['overcategory'] = sex.first().gender_for
		if sex is '' or sex.exists()==False:
			raise forms.ValidationError("Please, select a gender")
		return sex.first()

	def clean_undercategory(self):
		request = self.request
		data = self.cleaned_data
		print(data)
		data_undercat = self.cleaned_data.get('undercategory')
		undercategory = Undercategory.objects.filter(id=int(data_undercat))
		self.cleaned_data['category'] = undercategory.first().undercategory_for
		if undercategory is '' or undercategory.exists()==False:
			raise forms.ValidationError("Please, select a category")
		if self.cleaned_data['category'].category_for != data.get('sex'):
			raise forms.ValidationError("Please, select a valid category")
		return undercategory.first()
	
	def clean_size(self):
		request = self.request
		data = self.cleaned_data
		data_size = self.cleaned_data.get('size')
		size = Size.objects.filter(id=int(data_size))
		data_under = data.get('undercategory')
		if size is '' or size.exists()==False:
			raise forms.ValidationError("Please, select a size")
		if data_under is not None:
			if data_under.undercategory_for.category != size.first().size_for:
				raise forms.ValidationError("Please, select a valid size")
		return size.first()

	def clean_condition(self):
		request = self.request
		data_condition = self.cleaned_data.get('condition')
		condition = Condition.objects.filter(id=int(data_condition))
		if condition is '' or condition.exists()==False:
			raise forms.ValidationError("Please, select a condition")
		return condition.first()

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
			if chars > 400:
				charss = int(chars) - int(400)
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
		product.category = self.cleaned_data['category']
		product.overcategory = self.cleaned_data['overcategory']
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
		brand = Brand.objects.get(id=product.brand.id)
		undercategory = Undercategory.objects.get(id=product.undercategory.id)
		gender = Gender.objects.get(id=product.sex.id)
		size = Size.objects.get(id=product.size.id)
		condition = Condition.objects.get(id=product.condition.id)
		description = product.description
		self.initial['brand']=brand.brand_name
		self.initial['undercategory']=undercategory.undercategory
		self.initial['sex']=gender.gender
		self.initial['size']=size.size
		self.initial['condition']=condition.condition
		self.fields['sex'].widget.attrs['overcategory'] = gender.gender_for.overcategory
		self.fields['sex'].widget.attrs['gender'] = gender.gender
		self.fields['sex'].widget.attrs['id_for_upd'] = gender.id
		self.fields['undercategory'].widget.attrs['category'] = undercategory.undercategory_for.category
		self.fields['undercategory'].widget.attrs['undercategory'] = undercategory.undercategory
		self.fields['undercategory'].widget.attrs['id_for_upd'] = undercategory.id
		self.fields['size'].widget.attrs['id_for_upd'] = size.id
		self.fields['size'].widget.attrs['size'] = size.size
		self.fields['condition'].widget.attrs['category'] = undercategory.undercategory_for.category
		self.fields['condition'].widget.attrs['id_for_upd'] = condition.id
		self.fields['condition'].widget.attrs['condition'] = condition.condition
		if request.session.get('language') == 'RU':
			self.initial['undercategory']=undercategory.undercategory_ru
			self.initial['sex']=gender.gender_ru
			self.initial['condition']=condition.condition_ru
		elif request.session.get('language') == 'EN':
			self.initial['undercategory']=undercategory.undercategory_eng
			self.initial['sex']=gender.gender_eng
			self.initial['condition']=condition.condition_eng
		elif request.session.get('language') == 'UA':
			self.initial['undercategory']=undercategory.undercategory_ua
			self.initial['sex']=gender.gender_ua
			self.initial['condition']=condition.condition_ua















