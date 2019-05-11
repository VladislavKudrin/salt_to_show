from django.conf import settings
from django.db.models import Q
import random
import os
from django.db import models
from ecommerce.utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save
from django.urls import reverse





def get_filename_ext(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext


def upload_image_path(instance, filename):
	print(instance)
	print(filename)
	new_filename = random.randint(1,31231231)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
	return "products/{new_filename}/{final_filename}".format(
		new_filename=new_filename,
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

	def by_category_gender(self, query_category, query_gender):
		# for x in query:
		lookups_gender=(Q(category__iexact='nothing'))
		for x in query_gender:
			lookups_gender=lookups_gender|(Q(sex__iexact=x))
		filtered_gender = self.filter(lookups_gender)
		print(filtered_gender)
		lookups_category=(Q(category__iexact='nothing'))
		for x in query_category:
			lookups_category=lookups_category|(Q(category__iexact=x))
		# for x in query:
		# 	qs[x] = Product.objects.filter(category=x)
		# print(qs)
		# for product in qs:
		# 	print(product)
		if len(query_category)==0:
			return self.filter(lookups_gender)
		if len(query_gender) == 0:
			return self.filter(lookups_category)
		return filtered_gender.filter(lookups_category)

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
	def by_category_gender(self, query_category, query_gender):
		return self.get_queryset().by_category_gender(query_category, query_gender)
	def search(self, query):
		return self.get_queryset().active().search(query)

User=settings.AUTH_USER_MODEL

CATEGORY_CHOICES = (
	('tops', 'Tops'),
	('bottoms', 'Bottoms'),
	('accessories', 'Accessories'),
	('outwear', 'Outwear'),
	('footwear', 'Footwear'),
	)
SEX_CHOICES = (
	('man', 'Man'),
	('woman', 'Woman'),
	('unisex', 'Unisex')
	)
class Product(models.Model):
	user 			= models.ForeignKey(User, null=True, blank=True)
	title 			= models.CharField(max_length = 120)
	slug			= models.SlugField(default=None, unique = True, blank=True)
	description 	= models.TextField()
	price 			= models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
	featured		= models.BooleanField(default=False)
	active			= models.BooleanField(default=True)
	timestamp		= models.DateTimeField(auto_now_add=True)
	category 		= models.CharField(max_length=120, default='all', choices=CATEGORY_CHOICES)
	sex 			= models.CharField(max_length=120, default='not picked', choices=SEX_CHOICES)



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

	def get_absolute_url_for_delete(self):
		#return "/products/{slug}/".format(slug=self.slug)
		return reverse('products:delete', kwargs={"slug":self.slug}) #url products look for name delete

	def __str__(self):
		return self.title



def product_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_reciever,sender=Product)


class Image(models.Model):
	product 		= models.ForeignKey(Product, default=None, related_name='images')
	image			= models.ImageField(upload_to=upload_image_path, null=True, blank=True)

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











