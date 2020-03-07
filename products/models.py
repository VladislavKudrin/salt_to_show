from io import BytesIO
from PIL import Image
from django.core.files import File

from django.conf import settings
from django.db.models import Q
import random
import os
from django.db import models
from ecommerce.utils import unique_slug_generator, unique_image_id_generator
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from currency_converter import CurrencyConverter

from categories.models import Size, Brand, Undercategory, Gender, Category, Overcategory, Condition



class ImageOrderUtil(models.Model):
	slug			= models.SlugField(default=None, unique = True, blank=True)
	order_sequence  = models.CharField(max_length=120, blank=True, null=True)
	def __str__(self):
		return self.slug

    
def get_filename_ext(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext


def upload_image_path(instance, filename):
	product_slug = instance.product.slug
	new_filename = random.randint(1,31231231)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
	return "products/{new_filename}/{final_filename}".format(
		new_filename=product_slug,
		final_filename=final_filename)

class ProductQuerySet(models.query.QuerySet):#создание отсеяных списков, дополняют метод "геткверисет"
	def by_user(self, user):
		return self.filter(user=user)
	def active(self):
		return self.filter(active=True)
	def featured(self):
		return self.filter(featured=True)
	def search(self,query):
		lookups=(Q(title__icontains=query)
				|Q(description__icontains=query)
				)
		return self.filter(lookups).distinct()
	def filter_categories(self, lookup):
		if len(lookup) == 1:
			return self
		else:
			return self.filter(lookup)
	def filter_undercategory_size(self, qs, list_brand=None, list_condition=None, list_category = None, list_undercategory = None, list_size=None, link_codiert=None):
		arr=[]
		if list_brand is not None:
			lookups_brand=(Q(title__iexact='qwerty123'))
			if link_codiert is not None:
				link_codiert = link_codiert+"brand="
			for i, id_ in enumerate(list_brand):
				print(id_)
				brand = Brand.objects.get(id=int(id_))
				arr.append(brand)
				lookups_brand = lookups_brand|(Q(brand=brand))
				if link_codiert:
					if i+1 == len(list_brand):
						link_codiert = link_codiert+"{id_brand}".format(id_brand=int(id_))+'&'
					else: 
						link_codiert = link_codiert+"{id_brand}".format(id_brand=int(id_))+'+'
			qs = qs.filter(lookups_brand)
		if list_condition is not None:
			print(list_condition)
			print(qs)
			lookups_condition=(Q(title__iexact='qwerty123'))
			if link_codiert is not None:
				link_codiert = link_codiert+"condition="
			for i, id_ in enumerate(list_condition):
				condition = Condition.objects.get(id=int(id_))
				arr.append(condition)
				lookups_condition = lookups_condition|(Q(condition=condition))
				if link_codiert:
					if i+1 == len(list_condition):
						link_codiert = link_codiert+"{id_condition}".format(id_condition=int(id_))+'&'
					else: 
						link_codiert = link_codiert+"{id_condition}".format(id_condition=int(id_))+'+'
			qs = qs.filter(lookups_condition)
			print(qs)
		if list_category is not None:
			lookups_category=(Q(title__iexact='qwerty123'))
			if link_codiert:
				link_codiert = link_codiert+"category="
			for i, id_ in enumerate(list_category):
				category = Category.objects.get(id=int(id_))
				arr.append(category)
				lookups_category = lookups_category|(Q(category=category))
				if link_codiert:
					if i+1 == len(list_category):
						link_codiert = link_codiert+"{id_category}".format(id_category=int(id_))+'&'
					else: 
						link_codiert = link_codiert+"{id_category}".format(id_category=int(id_))+'+'
			qs = qs.filter(lookups_category)
		if list_undercategory is not None:
			lookups_undercategory=(Q(title__iexact='qwerty123'))
			if link_codiert:
				link_codiert = link_codiert+"undercategory="
			for i, id_ in enumerate(list_undercategory):
				undercategory = Undercategory.objects.get(id=int(id_))
				arr.append(undercategory)
				lookups_undercategory = lookups_undercategory|(Q(undercategory=undercategory))
				if link_codiert:
					if i+1 == len(list_undercategory):
						link_codiert = link_codiert+"{id_undercategory}".format(id_undercategory=int(id_))+'&'
					else: 
						link_codiert = link_codiert+"{id_undercategory}".format(id_undercategory=int(id_))+'+'
			qs = qs.filter(lookups_undercategory)
		if list_size is not None:
			print(list_size)
			lookups_size=(Q(title__iexact='qwerty123'))
			if link_codiert:
				link_codiert = link_codiert+"size="
			for i, id_ in enumerate(list_size):
				size = Size.objects.get(id=int(id_))
				arr.append(size)
				lookups_size = lookups_size|(Q(size=size))
				if link_codiert:
					if i+1 == len(list_size):
						link_codiert = link_codiert+"{id_size}".format(id_size=int(id_))
					else: 
						link_codiert = link_codiert+"{id_size}".format(id_size=int(id_))+'+'
			qs = qs.filter(lookups_size)
		return qs, link_codiert, arr


	def by_category_gender(self, query_category, query_gender, query_size, qs_brand):
		lookups_brand=(Q(category__iexact='nothing'))
		for x in qs_brand:
			lookups_brand=lookups_brand|(Q(brand=x))
		filtered_brand = self.filter(lookups_brand)
		lookups_gender=(Q(category__iexact='nothing'))
		for x in query_gender:
			lookups_gender=lookups_gender|(Q(sex__iexact=x))
		filtered_gender = self.filter(lookups_gender)
		lookups_category=(Q(category__iexact='nothing'))
		for x in query_category:
			lookups_category=lookups_category|(Q(category__iexact=x))
		filtered_category = self.filter(lookups_category)
		lookups_size=(Q(category__iexact='nothing'))
		for x in query_size:
			lookups_size=lookups_size|(Q(size=x))
		x_b = self.filter_categories(lookups_brand).filter_categories(lookups_gender).filter_categories(lookups_category).filter_categories(lookups_size)
		return(x_b)

	def authentic(self):
		return self.filter(authentic='authentic').exclude(order__status='paid')
	def fake(self):
		return self.filter(authentic='fake')	

class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def by_user(self, user):
		return self.get_queryset().by_user(user=user)
	def all(self):
		return self.get_queryset().active()#переписываем метод 
	def featured(self):
		return self.get_queryset().featured()

	def get_by_id(self, id):
		qs=self.get_queryset().filter(id=id)
		if qs.count() == 1:
			return qs.first()
		return None
	def filter_undercategory_size(self, qs, list_brand=None, list_condition=None, list_category = None, list_undercategory = None, list_size=None, link_codiert=None):
		return self.get_queryset().filter_undercategory_size(qs, list_brand, list_condition, list_category, list_undercategory, list_size, link_codiert)
	def by_category_gender(self, query_category, query_gender, query_size, qs_brand):
		return self.get_queryset().by_category_gender(query_category, query_gender, query_size, qs_brand)
	def search(self, query):
		return self.get_queryset().active().search(query)
	def filter_from_link_or_ajax(self, qs, linked=False, list_brand=None, list_condition=None, list_price=None,list_overcategory=None,list_gender = None, list_category = None, list_undercategory=None, list_size=None, user=None):
		context={}
		link_codiert=''
		data_brand = list_brand
		if data_brand:
			qs, link_codiert, instance_brand = Product.objects.filter_undercategory_size(qs=qs, list_brand=data_brand, link_codiert=link_codiert)
			context['brand_instance']=instance_brand
		data_condition = list_condition
		if data_condition:
			qs, link_codiert, instance_condition = Product.objects.filter_undercategory_size(qs=qs, list_condition=data_condition, link_codiert=link_codiert)
			context['condition_instance']=instance_condition
		data_price = list_price
		if data_price:
			price_min = data_price[0]
			price_max = data_price[1]
			context['price_min']=price_min
			context['price_max']=price_max
			if user:
				if user.is_authenticated():
					if price_min:
						price_min = Product.objects.price_to_region_price(user=user, price = price_min)
					if price_max:
						price_max = Product.objects.price_to_region_price(user=user, price = price_max)
			if not price_min and price_max:
				qs = qs.filter(price__lte=price_max)
				link_codiert = link_codiert + "price=+{price}".format(price=data_price[1])+'&'
			elif not price_max and price_min:
				qs = qs.filter(price__gte=price_min)
				link_codiert = link_codiert + "price={price}+".format(price=data_price[0])+'&'
			elif price_max and price_min:
				lookups_price = Q(price__gte=price_min)&Q(price__lte=price_max)
				qs = qs.filter(lookups_price)
				link_codiert = link_codiert + "price={price_min}+{price_max}".format(price_min=data_price[0], price_max=data_price[1])+'&'
		data_overcategory = list_overcategory
		if data_overcategory:
			overcategory_instance = Overcategory.objects.get(id=int(data_overcategory))
			context['overcategory_instance']=overcategory_instance
			qs = qs.filter(overcategory=overcategory_instance)
			link_codiert = link_codiert + "overcategory={id_overcategory}".format(id_overcategory=int(data_overcategory)) + '&'
		data_gender = list_gender
		if data_gender:
			gender_instance = Gender.objects.get(id=int(data_gender))
			context['gender_instance']=gender_instance
			qs = qs.filter(sex=gender_instance)
			link_codiert = link_codiert + "gender={id_gender}".format(id_gender=int(data_gender)) + '&'
		data_category = list_category
		if data_category:
			qs_cat, link_codiert, instance_category = Product.objects.filter_undercategory_size(qs=qs, list_category=data_category, link_codiert = link_codiert)
			context['category_instance']=instance_category
		data_undercategory = list_undercategory
		if data_undercategory:
			qs_undercat, link_codiert, instance_undercategory = Product.objects.filter_undercategory_size(qs=qs, list_undercategory=data_undercategory, link_codiert = link_codiert)
			context['undercategory_instance']=instance_undercategory
		if data_undercategory and data_category:
			qs = qs_cat.union(qs_undercat)
		elif data_category and not data_undercategory:
			qs=qs_cat
		elif data_undercategory and not data_category:
			qs=qs_undercat
		data_size = list_size
		if data_size:
			qs, link_codiert, instance_size = Product.objects.filter_undercategory_size(qs=qs, list_size=data_size, link_codiert=link_codiert)
			context['size_instance']=instance_size
		return qs, link_codiert, context

	def authentic(self):
		return self.get_queryset().active().authentic()

	def fake(self):
		return self.get_queryset().active().fake()
	def price_to_region_price(self, user, price):
		region_user = user.region
		if region_user:
			price = round((int(price)/region_user.currency_mult),6)
		return price


User=settings.AUTH_USER_MODEL



# CONDITION_CHOICES = (
# 	('item condition', 'Select an item condition'),
# 	('new with tags', 'New with tags'),
# 	('gently used', 'Gently used'),
# 	('used', 'Used'),
# 	)


AUTHENTICITY_CHOICES = (
	('undefined', 'Undefined'),
	('fake', 'Fake'),
	('authentic', 'Authentic'),
	)


class Product(models.Model):
	user                   = models.ForeignKey(User, null=True, blank=True)
	title                  = models.CharField(max_length = 120)
	slug                   = models.SlugField(default=None, unique = True, blank=True)
	description            = models.TextField()
	price                  = models.DecimalField(decimal_places=6, max_digits=16, default=0)
	featured               = models.BooleanField(default=False)
	active                 = models.BooleanField(default=True)
	timestamp              = models.DateTimeField(auto_now_add=True)
	category               = models.ForeignKey(Category, blank = True, null=True)
	sex                    = models.ForeignKey(Gender, blank = True, null=True)
	condition              = models.ForeignKey(Condition, blank = True, null=True)
	size                   = models.ForeignKey(Size, blank=False, null=True)
	brand                  = models.ForeignKey(Brand, blank=False, null=True)
	undercategory          = models.ForeignKey(Undercategory, blank = False, null=True)
	overcategory           = models.ForeignKey(Overcategory, blank = True, null=True)
	authentic              = models.CharField(max_length=120, default='undefined', choices=AUTHENTICITY_CHOICES, null=True)
	national_shipping      = models.DecimalField(decimal_places=6, max_digits=16, default=0, blank=False, null=True)
	international_shipping = models.DecimalField(decimal_places=6, max_digits=16, default=0, blank=True, null=True)



	objects = ProductManager()
	
	def make_total(self):
		national_shipping = 0
		international_shipping = 0
		price = 0
		if self.national_shipping:
			national_shipping = self.national_shipping
		if self.international_shipping:
			international_shipping = self.international_shipping
		if self.price:
			price = self.price
		return national_shipping + price

	def get_absolute_url(self):
		#return "/products/{slug}/".format(slug=self.slug)
		return reverse('products:detail', kwargs={"slug":self.slug})

	def get_absolute_url_for_update(self):
		#return "/products/{slug}/".format(slug=self.slug)
		return reverse('products:update', kwargs={"slug":self.slug})
	def get_absolute_url_for_delete(self):
		#return "/products/{slug}/".format(slug=self.slug)
		return reverse('products:delete', kwargs={"slug":self.slug})


	def __str__(self):
		return self.title

def product_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_reciever,sender=Product)

def product_post_save_reciever(sender, created, instance, *args, **kwargs):
	if not created:
		product = ProductThumbnail.objects.filter(product=instance)
		if not product.exists():
			ProductThumbnail.objects.create_update_thumbnail(product=instance)

post_save.connect(product_post_save_reciever, sender=Product)

class ProductImage(models.Model):
	product 		= models.ForeignKey(Product, default=None, related_name='images')
	image			= models.ImageField(upload_to=upload_image_path, null=True, blank=True)
	image_order 	= models.DecimalField(decimal_places=0, max_digits=20, default=1)
	slug			= models.SlugField(default=None, null=True, blank=False)
	unique_image_id = models.CharField(max_length = 120, default=None, unique = True, blank=False, null=True)
	def __str__(self):
		return self.product.title + str(self.image_order)
	def rotate_image(self, image, rotated_x=0):
		if rotated_x:
			int_rotated = int(rotated_x)
			if int_rotated != 0 or int_rotated%4 != 0:
				im = Image.open(image)
				image_rotated = im.rotate(-90*int_rotated, expand=True)
				img_io = BytesIO()
				image_rotated.save(img_io, im.format)
				new_image = File(img_io, name=str(image))
				self.image = new_image
				self.save()
		# 	return new_image
		# return image



def image_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.unique_image_id:
		instance.unique_image_id = unique_image_id_generator(instance, 'product_image')

pre_save.connect(image_pre_save_reciever,sender=ProductImage)

class ProductThumbnailManager(models.Manager):
	def create_update_thumbnail(self, product):
		first_image_model = ProductImage.objects.filter(slug=product.slug, image_order=1).first()
		first_image = first_image_model.image
		first_image_pil = Image.open(first_image)
		im_io = BytesIO() 
		size = settings.IMAGES_THUMBNAIL_SIZE
		first_image_pil.thumbnail(size)
		first_image_pil.save(im_io, first_image_pil.format , quality=settings.IMAGES_QUALITY_THUMBNAIL_PRECENTAGE) 
		new_image = File(im_io, name=product.slug+'.'+first_image_pil.format)
		thumb_exists = ProductThumbnail.objects.filter(product=product)
		if thumb_exists.exists():
			existing_thumb = thumb_exists.first()
			existing_thumb.thumbnail.delete()
			existing_thumb.thumbnail = new_image
			existing_thumb.save()
		else:
			ProductThumbnail.objects.create(
						product=product,
						thumbnail=new_image,
										)


class ProductThumbnail(models.Model):
	product = models.ForeignKey(Product, default=None, related_name='thumbnail')
	thumbnail = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
	objects = ProductThumbnailManager()
	def __str__(self):
		return self.product.slug + ' thumbnail'

# def thumbnail_post_save_reciever(sender, created, instance, *args, **kwargs):
# 	if created:


# post_save.connect(thumbnail_post_save_reciever,sender=ProductThumbnail)

class ReportedProduct(models.Model):
	user    	= models.ForeignKey(User, related_name='reporter')
	product 	= models.ForeignKey(Product, related_name='reported_product')
	reason	 	= models.CharField(max_length=240, default=None, null=True)
	timestamp	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.product.title
		
# def product_create_post_save_reciever(sender, request, instance, *args, **kwargs):
# 	if request.user.is_authenticated():
# 		user = request.user
# 		instance.user = user
# 	else:
# 		instance.delete()
# 		raise ValidationError("You need to be Logged In")


# post_save.connect(product_create_post_save_reciever, sender= Product)








