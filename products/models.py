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

from categories.models import Size, Brand

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
				|Q(price__icontains=query)
				|Q(tag__title__icontains=query)

				)
		return self.filter(lookups).distinct()

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
		if len(query_category)==0 and len(query_gender)==0 and len(qs_brand)==0:
			return self.all()
		elif len(query_category)==0 and len(query_gender)==0:
			return self.filter(lookups_brand)
		elif len(query_category)==0 and len(qs_brand)==0:
			return self.filter(lookups_gender)
		elif len(query_gender) == 0 and len(query_size)==0:
			return self.filter(lookups_category)
		elif len(query_gender) == 0 and len(qs_brand)==0:
			return filtered_category.filter(lookups_size)
		elif len(query_category)==0:
			return filtered_brand.filter(lookups_gender)
		elif len(query_gender)==0 and len(query_size)==0:
			return filtered_brand.filter(lookups_category)
		elif len(query_gender)==0:
			return filtered_brand.filter(lookups_category).filter(lookups_size)
		elif len(query_size)==0:
			return filtered_brand.filter(lookups_gender).filter(lookups_category)
		elif len(query_gender) == 0:
			return filtered_category.filter(lookups_size)
		elif len(query_size)==0:
			return filtered_gender.filter(lookups_category)
		return filtered_brand.filter(lookups_gender).filter(lookups_category).filter(lookups_size)

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
	def by_category_gender(self, query_category, query_gender, query_size, qs_brand):
		return self.get_queryset().by_category_gender(query_category, query_gender, query_size, qs_brand)
	def search(self, query):
		return self.get_queryset().active().search(query)

User=settings.AUTH_USER_MODEL

CATEGORY_CHOICES = (
	('select a category', 'Select a category'),
	('tops', 'Tops'),
	('bottoms', 'Bottoms'),
	('accessories', 'Accessories'),
	('outerwear', 'Outerwear'),
	('footwear', 'Footwear'),
	)
SEX_CHOICES = (
	('man', 'Man'),
	('woman', 'Woman'),
	)
class Product(models.Model):
	user 			= models.ForeignKey(User, null=True, blank=True)
	title 			= models.CharField(max_length = 120)
	slug			= models.SlugField(default=None, unique = True, blank=True)
	description 	= models.TextField()
	price 			= models.DecimalField(decimal_places=2, max_digits=20, default=0)
	featured		= models.BooleanField(default=False)
	active			= models.BooleanField(default=True)
	timestamp		= models.DateTimeField(auto_now_add=True)
	category 		= models.CharField(max_length=120, default='all', choices=CATEGORY_CHOICES)
	sex 			= models.CharField(max_length=120, default='not picked', choices=SEX_CHOICES)
	size 			= models.ForeignKey(Size, blank=False, null=True)
	brand 			= models.ForeignKey(Brand, blank=True, null=True)


	objects = ProductManager()

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

class ProductImage(models.Model):
	product 		= models.ForeignKey(Product, default=None, related_name='images')
	image			= models.ImageField(upload_to=upload_image_path, null=True, blank=True)
	image_order 	= models.DecimalField(decimal_places=0, max_digits=20, default=1)
	slug			= models.SlugField(default=None, null=True, blank=False)
	unique_image_id = models.CharField(max_length = 120, default=None, unique = True, blank=False, null=True)
	def __str__(self):
		return self.product.title + str(self.image_order)



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
		size = 275, 275
		first_image_pil.thumbnail(size, Image.ANTIALIAS)
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


# def product_create_post_save_reciever(sender, request, instance, *args, **kwargs):
# 	if request.user.is_authenticated():
# 		user = request.user
# 		instance.user = user
# 	else:
# 		instance.delete()
# 		raise ValidationError("You need to be Logged In")


# post_save.connect(product_create_post_save_reciever, sender= Product)











