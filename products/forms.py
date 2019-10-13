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
		region_user = request.user.region
		if region_user:
			currency_placeholder = region_user.currency
		else:
			currency_placeholder = 'USD'
		self.lan = request.session.get('language')
		self.fields['sex'].widget.attrs['readonly'] = True
		self.fields['undercategory'].widget.attrs['readonly'] = True
		self.fields['size'].widget.attrs['readonly'] = True
		self.fields['condition'].widget.attrs['readonly'] = True
		self.fields['title'].widget.attrs['placeholder'] = 'Some keywords about your item'
		self.fields['description'].widget.attrs['placeholder'] = 'Describe your item in details'
		self.fields['price'].widget.attrs['placeholder'] = 'Enter a price in {currency}'.format(currency=currency_placeholder)
		self.fields['price'].initial = ''
		self.fields['sex'].label = 'Gender'
		if self.lan == 'RU':
			self.fields['title'].label = "Название"
			self.fields['title'].widget.attrs['placeholder'] = 'Пара слов про айтем'
			self.fields['description'].label = "Описание"
			self.fields['description'].widget.attrs['placeholder'] = 'Подробно опиши айтем'
			self.fields['price'].label = "Цена"
			self.fields['price'].widget.attrs['placeholder'] = 'Введи цену в {currency}'.format(currency=currency_placeholder)
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
		elif self.lan == 'UA':
			self.fields['title'].label = "Назва"
			self.fields['title'].widget.attrs['placeholder'] = 'Пара слів про айтем'
			self.fields['description'].label = "Опис"
			self.fields['description'].widget.attrs['placeholder'] = 'Детально опиши айтем'
			self.fields['price'].label = "Ціна"
			self.fields['price'].widget.attrs['placeholder'] = 'Введи ціну в {currency}'.format(currency=currency_placeholder)
			self.fields['brand'].label = "Бренд"
			self.fields['brand'].widget.attrs['placeholder'] = 'Вибери бренд'
			self.fields['sex'].label = "Гендер"
			self.fields['sex'].widget.attrs['placeholder'] = 'Вибери гендер'
			self.fields['undercategory'].label = "Категорія"
			self.fields['undercategory'].widget.attrs['placeholder'] = 'Вибери категорію'
			self.fields['condition'].widget.attrs['placeholder'] = 'Вибери стан'
			self.fields['size'].widget.attrs['placeholder'] = 'Вибери розмір'
			self.fields['size'].label = "розмір"
			self.fields['condition'].label = "Стан"


		
	def clean_sex(self):
		request = self.request
		data_sex = self.cleaned_data.get('sex')
		sex = Gender.objects.filter(id=int(data_sex))
		self.cleaned_data['overcategory'] = sex.first().gender_for
		if self.lan == 'RU':
			error_message = 'Пожалуйста, выбери гендер'
		elif self.lan == 'UA':
			error_message = "Please, select a gender"
		elif self.lan == 'EN':
			error_message = "Please, select a gender"
		if sex is '' or sex.exists()==False:
			self.add_error('sex', error_message)
		return sex.first()

	def clean_undercategory(self):
		request = self.request
		data = self.cleaned_data
		data_undercat = self.cleaned_data.get('undercategory')
		undercategory = Undercategory.objects.filter(id=int(data_undercat))
		self.cleaned_data['category'] = undercategory.first().undercategory_for
		if self.lan == 'RU':
			error_message = 'Пожалуйста, выбери подходящую категорию'
		elif self.lan == 'UA':
			error_message = "Please, select a valid category"
		elif self.lan == 'EN':
			error_message = "Please, select a valid category"
		if undercategory is '' or undercategory.exists()==False:
			self.add_error('undercategory', error_message)
		if self.cleaned_data['category'].category_for != data.get('sex'):
			self.add_error('undercategory', error_message)
		return undercategory.first()
	
	def clean_size(self):
		request = self.request
		data = self.cleaned_data
		data_size = self.cleaned_data.get('size')
		size = Size.objects.filter(id=int(data_size))
		data_under = data.get('undercategory')
		data_overcategory = data.get('sex').gender_for
		if self.lan == 'RU':
			error_message = 'Пожалуйста, выбери подходящий размер'
		elif self.lan == 'UA':
			error_message = "Please, select a valid size"
		elif self.lan == 'EN':
			error_message = "Please, select a valid size"
		if size is '' or size.exists()==False:
			self.add_error('size', error_message)
		if data_overcategory is not None or data_under is not None:
			if data_under.undercategory_for.category_for.gender_for != size.first().size_type or data_under.undercategory_for.category != size.first().size_for:
				self.add_error('size', error_message)
		return size.first()

	def clean_condition(self):
		request = self.request
		data_condition = self.cleaned_data.get('condition')
		condition = Condition.objects.filter(id=int(data_condition))
		if self.lan == 'RU':
			error_message = 'Пожалуйста, выбери состояние'
		elif self.lan == 'UA':
			error_message = "Please, select a condition"
		elif self.lan == 'EN':
			error_message = "Please, select a condition"
		if condition is '' or condition.exists()==False:
			self.add_error('condition', error_message)
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

			# if in element more than 35 symbols > count it as a line
			length = len(description.splitlines())

			for i in description.splitlines():
				length_of_line = int(len(i))
				if length_of_line > 35: # check if line too large 

					more_char = length_of_line - 35
					if more_char <= 35:
						length += 1
					else: 
						length += more_char // 35

			chars = len(description)
			if length > 14: 
				lines = int(length) - int(14)
				message = ' Please, make it shorter. # of lines to be removed: {lines}'.format(lines=lines)
				self.add_error('description', message)
			if chars > 400:
				charss = int(chars) - int(400)
				message = ' Please, make it shorter. # of characters to be removed: {charss}'.format(charss=charss)
				self.add_error('description', message)	
		return description
	def clean_price(self):
		data = self.cleaned_data
		price = data.get('price')
		user = self.request.user
		price = Product.objects.price_to_region_price(price = price, user = user)
		# if region_user:
		# 	price = round((int(price)/region_user.currency_mult),6)
		return price

class ImageForm(ProductCreateForm):
	image = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, 'class':'image-upload-button','accept':'image/*','id':'image_custom'} ))
	def __init__(self, request, *args, **kwargs):
		super(ImageForm, self).__init__(request, *args, **kwargs)
		self.fields['image'].label = "Images*"
		if request.session.get('language')=='RU':
			self.fields['image'].label = "Фото*"
		if request.session.get('language')=='UA':
			self.fields['image'].label = "Фото*"
	
	def clean_image(self):
		form_id = self.request.POST.get('form_id')
		cleaned_images = UploadedFile.objects.filter(form_id=form_id)
		if len(cleaned_images)==0:
			if self.lan == 'RU':
				raise forms.ValidationError("А фото айтема?")
			elif self.lan == 'UA':
				raise forms.ValidationError("А фото айтема?")
			else:
				raise forms.ValidationError("What about item's photos?")
		if len(cleaned_images)<settings.IMAGES_UPLOAD_MIN:
			if self.lan == 'RU':
				raise forms.ValidationError("Маловато фотографий. Попробуй 4 и больше!")
			elif self.lan == 'UA':
				raise forms.ValidationError("Маловато фотографій. Спробуй 4 і більше!")
			else:
				raise forms.ValidationError("Not enough photos. Try 4 and more!")	
		if len(cleaned_images)>settings.IMAGES_UPLOAD_LIMIT:
			if self.lan == 'RU':
				raise forms.ValidationError("Слишком много фотографий. 8 будет вполне достаточно!")
			elif self.lan == 'UA':
				raise forms.ValidationError("Занадто багато фотографій. 8 буде цілком достатньо!")
			else:
				raise forms.ValidationError("Too many photos, 8 would be enough!")	
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
				this_rotate = qs_rotate.get(str(file.file_id))
				file = UploadedFile.objects.rotate_image(image = file.uploaded_file.file, rotated_x = this_rotate)
				obj = ProductImage.objects.create(
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
		self.slug = slug
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
		if self.request.user.region:
			currency_mult = self.request.user.region.currency_mult
			price = round(product.price * currency_mult)
			self.initial['price']=price
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
	def save(self, commit=True):
			product = Product.objects.get(slug=self.slug)
			product.title = self.cleaned_data['title']
			product.brand = self.cleaned_data['brand']
			product.overcategory = self.cleaned_data['overcategory']
			product.sex = self.cleaned_data['sex']
			product.category = self.cleaned_data['category']
			product.undercategory = self.cleaned_data['undercategory']
			product.size = self.cleaned_data['size']
			product.condition = self.cleaned_data['condition']
			product.price = self.cleaned_data['price']
			product.description = self.cleaned_data['description']
			if commit:
				product.save()
			return product













