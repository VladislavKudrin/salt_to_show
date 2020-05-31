import random
import os

from django.conf import settings
from django.db.models import Q
from django.db import models

from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from datetime import date
from django.utils.safestring import mark_safe



from io import BytesIO
from PIL import Image
from imagekit.models import ProcessedImageField
from imagekit import processors 
from django.core.files import File

from ecommerce.utils import unique_slug_generator, price_to_region
from categories.models import Size, Brand, Undercategory, Gender, Category, Overcategory, Condition
from categories.utils import build_link_categories


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
				|Q(brand__brand_name__icontains=query)
				)
		return self.filter(lookups).distinct()

	def filter_categories(self, lookup):
		if len(lookup) == 1:
			return self
		else:
			return self.filter(lookup)
			
	def authentic(self):
		return self.filter(authentic='authentic')

	def fake(self):
		return self.filter(authentic='fake')

	def available(self):
		return self.exclude(order__status__in=['paid', 'shipped', 'refunded'])

	def payable(self):
		threshold = date(2020, 3, 1) # not possible to buy items older than this 1th of March 
		return self.filter(timestamp__gte=threshold)



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
	def search(self, query):
		return self.get_queryset().active().search(query)
	def authentic(self):
		return self.get_queryset().active().authentic()

	def fake(self):
		return self.get_queryset().active().fake()

	def payable(self):
		return self.get_queryset().payable()

	def get_categoried_queryset(self, request, linked_data=None):
		context={}
		if not linked_data:
			data_overcategory = request.GET.get('overcategory')
			data_gender = request.GET.get('gender')
			data_category = request.GET.getlist('category')
			data_undercategory = request.GET.getlist('undercategory')
			data_brand = request.GET.getlist('brand')
			data_price = request.GET.getlist('price')
			data_size = request.GET.getlist('size')
			data_condition = request.GET.getlist('condition')
			data_sort = request.GET.get('sort')
			link_codiert = build_link_categories(request)
		elif linked_data == 'all':
			queryset = Product.objects.all()
			return queryset, context
		else:
			data_overcategory = linked_data.get('overcategory') or None
			data_gender = linked_data.get('gender') or None
			data_category = linked_data.get('category') or None
			data_undercategory = linked_data.get('undercategory') or None
			data_brand = linked_data.get('brand') or None
			data_price = linked_data.get('price') or None
			data_size = linked_data.get('size') or None
			data_condition = linked_data.get('condition') or None
			data_sort = linked_data.get('sort') or None
			context = {
				'brand_instance'        :data_brand,
				'condition_instance'    :data_condition
			}
			try:
				context['price_min'] = data_price[0]
				context['price_max'] = data_price[1]
			except:
				pass
		if data_undercategory:
			queryset = Product.objects.select_related('undercategory').select_related('brand').select_related('size').all().filter(undercategory__id__in=data_undercategory)
		elif data_gender:
			queryset = Product.objects.select_related('sex').select_related('brand').select_related('size').all().filter(sex__id__in=data_gender)
		elif data_overcategory:
			queryset = Product.objects.select_related('overcategory').select_related('brand').select_related('size').all().filter(overcategory__id__in = data_overcategory)
		else:
			queryset = Product.objects.select_related('brand').select_related('size').all()

		if data_size:
			queryset = queryset.filter(size__id__in=data_size)
		if data_brand:
			queryset = queryset.filter(brand__id__in=data_brand)
		if data_condition:
			queryset = queryset.select_related('condition').filter(condition__id__in=data_condition)
		if data_price:
			price_min = data_price[0]
			price_max = data_price[1]
			if request.user.is_authenticated():
				if price_min:
					price_min = price_to_region(user=request.user, price = price_min)
				if price_max:
					price_max = price_to_region(user=request.user, price = price_max)
			else:
				if price_min:
					price_min = price_to_region(price = price_min)
				if price_max:
					price_max = price_to_region(price = price_max)
			if not price_min and price_max:
				queryset = queryset.filter(price__lte=price_max)
			elif not price_max and price_min:
				queryset = queryset.filter(price__gte=price_min)
			elif price_max and price_min:
				queryset = queryset.filter(price__range=(price_min, price_max))

		#filters
		#sort
		if data_sort == 'high':
			queryset=queryset.order_by('price')
		elif data_sort == 'low':
			queryset=queryset.order_by('-price')
		else:
			queryset=queryset.order_by('-timestamp')
		#sort
		if not linked_data:		
			return queryset, link_codiert
		else:
			return queryset, context 

User=settings.AUTH_USER_MODEL


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
	national_shipping      = models.DecimalField(decimal_places=0, max_digits=16, default=0, blank=False, null=True)
	international_shipping = models.DecimalField(decimal_places=6, max_digits=16, default=0, blank=True, null=True)
	price_original  	   = models.DecimalField(decimal_places=0, max_digits=16, default=0, blank=True, null=True)
	currency_original  	   = models.CharField(max_length = 120, default='undefined', blank=True, null=True)



	objects = ProductManager()
	
	
	def make_total(self):
		national_shipping = 0
		international_shipping = 0
		price = 0
		if self.national_shipping:
			national_shipping = self.national_shipping
		# if self.international_shipping:
		# 	international_shipping = self.international_shipping
		if self.price_original:
			price = self.price_original
		sum_ = national_shipping + price
		return sum_

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

	@property
	def is_active(self):
		return self.active

	@property
	def is_authentic(self):
		if self.authentic == 'authentic':
			return True
		else:
			return False

	@property
	def is_paid(self):
		try:
			order = self.order.first()
			return order.is_paid
		except:
			return False

	@property
	def is_payable(self):
		item = self.timestamp.date() # timestamp of item
		threshold = date(2020, 3, 1) # not possible to buy items older than this 1th of March 
		return item > threshold

def product_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_reciever,sender=Product)

# def product_post_save_reciever(sender, created, instance, *args, **kwargs):
# 	if not created:
# 		if instance.authentic == 'authentic':
# 			from bot.views import send_message_to_telegram_
# 			send_message_to_all_users(instance)
# post_save.connect(product_post_save_reciever,sender=Product)


class ProductImage(models.Model):
	product 		= models.ForeignKey(Product, default=None, related_name='images')
	image			= models.ImageField(upload_to=upload_image_path, null=True, blank=True)
	image_order 	= models.DecimalField(decimal_places=0, max_digits=20, default=1)
	slug			= models.SlugField(default=None, null=True, blank=False)
	def __str__(self):
		return self.product.title + str(self.image_order)

	def to_thumbnail(self):
		ProductThumbnail.objects.new_or_update(product=self.product, image=self.image)

	def image_tag(self):
		return mark_safe('<img src="%s" width="500" height="500" style="object-fit: contain;"" />' % (self.image.url))  # Get Image url

	image_tag.short_description = 'Image'


def product_image_post_save(sender, created, instance, *args, **kwargs):
	if instance.image_order == 1:
		instance.to_thumbnail()

post_save.connect(product_image_post_save, sender=ProductImage)



class ProductThumbnailManager(models.Manager):
	def new_or_update(self, product, image):
		obj = self.model.objects.filter(product=product)
		with Image.open(image) as first_image_pil:
			im_io = BytesIO() 
			size = settings.IMAGES_THUMBNAIL_SIZE
			first_image_pil.thumbnail(size)
			first_image_pil.save(im_io, first_image_pil.format , quality=settings.IMAGES_QUALITY_THUMBNAIL_PRECENTAGE) 
			new_image = File(im_io, name=product.slug+'.'+first_image_pil.format)	
			if obj.exists():
				if obj.count() == 1:
					thumbnail=obj.first()
					thumbnail.thumbnail.delete()
					thumbnail.thumbnail = new_image
					thumbnail.save()
				else: 
					obj.delete()
					ProductThumbnail.objects.create(
							product=product,
							thumbnail=new_image,
											)
			else:
				ProductThumbnail.objects.create(
							product=product,
							thumbnail=new_image,
											)

class ProductThumbnail(models.Model):
	product = models.ForeignKey(Product, default=None, related_name='thumbnail')
	thumbnail = ProcessedImageField(upload_to=upload_image_path,
                                           processors=[
                                           processors.Thumbnail(600, 600, crop=False)],
                                           format='JPEG',
                                           options={'quality': 100}, null=True)
	objects = ProductThumbnailManager()
	def __str__(self):
		return self.product.slug + ' thumbnail'



	def get_absolute_url(self):
		return settings.BASE_URL + self.thumbnail.url








class ReportedProduct(models.Model):
	user    	= models.ForeignKey(User, related_name='reporter')
	product 	= models.ForeignKey(Product, related_name='reported_product')
	reason	 	= models.CharField(max_length=240, default=None, null=True)
	timestamp	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.product.title







