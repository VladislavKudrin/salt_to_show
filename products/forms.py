import re

from django.http import JsonResponse
from django import forms
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.validators import validate_image_file_extension
from django.conf import settings
from django.utils.translation import gettext as _




from betterforms.multiform import MultiModelForm
from image_uploader.validators import validate_file_extension
from imagekit.processors import Transpose
from django.core.files import File


from image_uploader.utils import rotate_image
from addresses.forms import AddressForm
from accounts.forms import UserDetailChangeForm
from billing.forms import CardForm
from .models import Product, ImageOrderUtil, ProductImage
from categories.models import Size, Brand, Undercategory, Overcategory, Gender, Category, Condition
from ecommerce.utils import random_string_generator, price_to_region

class ProductCreateForm(forms.ModelForm):
	brand = forms.CharField(label=_('Brand'), required=True, widget=forms.TextInput(attrs={"class":'form-control brandautofill'}))
	sex = forms.CharField(required=True, widget=forms.TextInput(attrs={"class":"custom-readonly"}))
	undercategory = forms.CharField(required=True, widget=forms.TextInput(attrs={"class":"custom-readonly"}))
	size = forms.CharField(required=True, widget=forms.TextInput(attrs={"class":"custom-readonly"}))
	condition = forms.CharField(required=True, widget=forms.TextInput(attrs={"class":"custom-readonly"}))
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
		'national_shipping',
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
		# self.fields['shipping_price'].widget.attrs['class'] = 'custom-readonly'
		self.fields['size'].widget.attrs['readonly'] = True
		self.fields['condition'].widget.attrs['readonly'] = True
		self.fields['title'].widget.attrs['placeholder'] = _('Some keywords about your item')
		self.fields['description'].widget.attrs['placeholder'] = _('Describe your item in details')
		# self.fields['price'].widget.attrs['placeholder'] = _('Price in ') + ('{currency}').format(currency=currency_placeholder)
		# self.fields['national_shipping'].widget.attrs['placeholder'] = _('National shipping costs')
		self.fields['brand'].widget.attrs['placeholder'] = _('Select a brand')
		self.fields['sex'].widget.attrs['placeholder'] = _('Gender')
		self.fields['undercategory'].widget.attrs['placeholder'] = _('Category')
		self.fields['size'].widget.attrs['placeholder'] = _('Size')
		self.fields['condition'].widget.attrs['placeholder'] = _('Condition')
		self.fields['price'].initial = ''
		self.fields['national_shipping'].initial = ''
		self.fields['title'].label = False
		self.fields['sex'].label = False
		self.fields['undercategory'].label = False
		self.fields['size'].label = False
		self.fields['condition'].label = False
		self.fields['price'].label = _('Price in ') + ('{currency}').format(currency=currency_placeholder)
		self.fields['national_shipping'].label = _('Shipping price in ') + ('{currency}').format(currency=currency_placeholder)
		self.fields['description'].label = False
		self.fields['brand'].label = False
		self.fields['price'].widget.attrs['step'] = 1
		self.fields['national_shipping'].widget.attrs['step'] = 1
		self.fields['price'].widget.attrs['class'] = 'labels-placement'
		self.fields['national_shipping'].widget.attrs['class'] = 'labels-placement'
		if request.user.is_admin:
			self.fields['price'].initial = 123
			self.fields['national_shipping'].initial = 123
			self.fields['title'].initial = 'оооо Макарена'
			self.fields['description'].initial = 'Макареночка с маслом и сырником'
			self.fields['brand'].initial = 'Boris Bidjan Saberi'




		
	def clean_sex(self):
		request = self.request
		data_sex = self.cleaned_data.get('sex')
		sex = Gender.objects.filter(id=int(data_sex))
		error_message = _("Please, select a gender")
		if sex is '' or sex.exists()==False:
			self.add_error('sex', error_message)
		else:
			self.cleaned_data['overcategory'] = sex.first().gender_for
		return sex.first()

	def clean_undercategory(self):
		request = self.request
		data = self.cleaned_data
		data_undercat = self.cleaned_data.get('undercategory')
		undercategory = Undercategory.objects.filter(id=int(data_undercat))
		self.cleaned_data['category'] = undercategory.first().undercategory_for
		error_message = _("Please, select a valid category")
		if undercategory is '' or undercategory.exists()==False:
			self.add_error('undercategory', error_message)
		if self.cleaned_data['category'].category_for != data.get('sex'):
			self.add_error('undercategory', error_message)
		return undercategory.first()
	
	def clean_size(self):
		request = self.request
		data_sex = self.cleaned_data.get('sex')
		if data_sex is not None:
			data_overcategory = self.cleaned_data.get('sex').gender_for
		else:
			data_overcategory = None
		data_size = self.cleaned_data.get('size')
		size = Size.objects.filter(id=int(data_size))
		data_under = self.cleaned_data.get('undercategory')
		error_message = _("Please, select a valid size")
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
		error_message = _("Please, select a condition")
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
			self.add_error('brand', _('Please, select existing brand'))

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
			if length > 18: 
				lines = int(length) - int(18)
				message = _('Please, make it shorter. # of lines to be removed:') + '{lines}'.format(lines=lines)
				self.add_error('description', message)
			if chars > 400:
				charss = int(chars) - int(400)
				message = _('Please, make it shorter. # of characters to be removed:') + "{charss}".format(charss=charss)
				self.add_error('description', message)	
		return description
	def clean_price(self):
		data = self.cleaned_data
		price = data.get('price')
		self.cleaned_data['price_original'] = price
		user = self.request.user
		price = price_to_region(price = price, user = user)
		return price

	# def clean_national_shipping(self):
	# 	user = self.request.user
	# 	national_shipping = Product.objects.price_to_region_price(price = self.cleaned_data.get('national_shipping'), user = user)
	# 	return national_shipping

class ImageForm(ProductCreateForm):
	image = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, 'class':'image-upload-button','accept':'image/*','id':'image_custom'} ))
	def __init__(self, request, *args, **kwargs):
		super(ImageForm, self).__init__(request, *args, **kwargs)
		self.fields['image'].label = _("Images*")
	def clean_image(self):
		images = self.request.FILES.getlist('image')
		rotateTimes = self.request.POST.getlist('rotateTimes')
		cleaned_images = []
		for idx, image in enumerate(images):
			if rotateTimes[idx] != 0:
				img = rotate_image(image, rotateTimes[idx])
				cleaned_images.append(img)
		if len(cleaned_images)==0:
			raise forms.ValidationError(_("Upload at least 4 images"))
		if len(cleaned_images)<settings.IMAGES_UPLOAD_MIN:
			raise forms.ValidationError(_("Not enough photos. Minimal amount - 4"))
		if len(cleaned_images)>settings.IMAGES_UPLOAD_LIMIT:
			raise forms.ValidationError(_("Too many files, max. amount 8"))
		return cleaned_images
		
	def save(self, commit=True):
		product = super(ProductCreateForm, self).save(commit=False)
		product.user = self.request.user
		product.category = self.cleaned_data['category']
		product.overcategory = self.cleaned_data['overcategory']
		product.active = True
		form_id = self.request.POST.get('form_id')
		product.price_original = self.cleaned_data['price_original']
		product.currency_original = self.request.user.region.currency
		if self.request.user.is_admin:
			product.authentic = 'authentic'
		if commit:
			product.save()
			images = self.cleaned_data['image']
			if images:
				for idx, file in enumerate(images):
					obj = ProductImage.objects.create(
						product=product,
						image=file,
						slug=product.slug,
						image_order=idx+1
										)
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
		price = product.price_original
		self.initial['brand']=brand.brand_name
		self.initial['sex']=_(gender.gender_eng)
		self.initial['undercategory']=_(undercategory.undercategory_eng)
		self.initial['size']=size.size
		self.initial['condition']=_(condition.condition_eng)
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
		self.initial['price']=price

	def clean_image(self):
		pass

	def clean(self):
		images = ProductImage.objects.filter(slug=self.slug)
		#doesnt work with just order by, because we change instances and queryset changes too
		keyArray = self.request.POST.getlist('keyArray')
		rotate_arr = self.request.POST.getlist('rotateTimes')
		if len(keyArray) > 0:
			img_dict = {}
			for image in images:
				img_dict[str(image.image_order)] = image
			for idx, order in enumerate(keyArray):
				img = img_dict.get(order)
				rotate = int(rotate_arr[idx])
				if rotate != 0:
					image = rotate_image(image = img.image, rotated_x = rotate)
					img.image = image
				img.image_order = idx + 1
				img.save()
				
	def save(self, commit=True):
		product                   = Product.objects.get(slug=self.slug)
		product.title             = self.cleaned_data['title']
		product.brand             = self.cleaned_data['brand']
		product.overcategory      = self.cleaned_data['overcategory']
		product.sex               = self.cleaned_data['sex']
		product.category          = self.cleaned_data['category']
		product.undercategory     = self.cleaned_data['undercategory']
		product.size              = self.cleaned_data['size']
		product.condition         = self.cleaned_data['condition']
		product.price             = self.cleaned_data['price']
		product.description       = self.cleaned_data['description']
		product.national_shipping = self.cleaned_data['national_shipping']
		product.price_original    = self.cleaned_data['price_original']
		if commit:
			product.save()
		return product





class CheckoutMultiForm(MultiModelForm): #https://django-betterforms.readthedocs.io/en/latest/multiform.html#working-with-modelforms
    form_classes = {
    'address_form' : AddressForm,
    'card_form': CardForm,
    }  







