from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse


from django.db.models.signals import pre_save

from .utils import unique_slug_url_shortener_generator



class Overcategory(models.Model):
	overcategory 		= models.CharField(max_length=120, blank=True)
	overcategory_ru 	= models.CharField(max_length=120, blank=True)
	overcategory_eng 	= models.CharField(max_length=120, blank=True)
	overcategory_ua 	= models.CharField(max_length=120, blank=True)
	def __str__(self):
		return self.overcategory
	def get_absolute_url(self):
		return reverse('products:list') + 'overcategory='+str(self.id)

class Gender(models.Model):
	gender_for 	= models.ForeignKey(Overcategory)
	gender_admin = models.CharField(max_length=120, blank=True)
	gender 		= models.CharField(max_length=120, blank=True)
	gender_ru 	= models.CharField(max_length=120, blank=True)
	gender_eng 	= models.CharField(max_length=120, blank=True)
	gender_ua 	= models.CharField(max_length=120, blank=True)
	def __str__(self):
		return (self.gender)
	def get_absolute_url(self):
		return reverse('products:list') + 'overcategory='+str(self.gender_for.id) + '&gender='+str(self.id)

class Category(models.Model):
	category_for 	= models.ForeignKey(Gender)
	category_admin 	= models.CharField(max_length=120, blank=True)
	category 		= models.CharField(max_length=120, blank=True)
	category_ru 	= models.CharField(max_length=120, blank=True)
	category_eng 	= models.CharField(max_length=120, blank=True)
	category_ua 	= models.CharField(max_length=120, blank=True)
	def __str__(self):
		return (self.category)
	def get_absolute_url(self):
		return reverse('products:list') + 'overcategory='+str(self.category_for.gender_for.id) + '&gender='+str(self.category_for.id) + '&category='+str(self.id)
class Undercategory(models.Model):
	undercategory_for 	= models.ForeignKey(Category)
	undercategory_admin = models.CharField(max_length=120, blank=True)
	undercategory 		= models.CharField(max_length=120, blank=True)
	undercategory_ru 	= models.CharField(max_length=120, blank=True)
	undercategory_eng 	= models.CharField(max_length=120, blank=True)
	undercategory_ua 	= models.CharField(max_length=120, blank=True)
	def __str__(self):
		return (self.undercategory)
	def get_absolute_url(self):
		return reverse('products:list') + 'overcategory='+str(self.undercategory_for.category_for.gender_for.id) + '&gender='+str(self.undercategory_for.category_for.id) + '&undercategory='+str(self.id)
class Size(models.Model):
	size_for 		= models.CharField(max_length=120, blank=True)
	size_admin 		= models.CharField(max_length=120, blank=True)
	size 			= models.CharField(max_length=120, blank=True)
	size_kids 		= models.CharField(max_length=120, blank=True)
	size_type 		= models.ForeignKey(Overcategory, blank = True, null=True)
	def __str__(self):
		return (self.size + '_'+self.size_for+'_')

class Brand(models.Model):
	brand_name = models.CharField(max_length=120, blank=True)
	def __str__(self):
		return self.brand_name
	def get_absolute_url(self):
		return reverse('products:list') + 'brand='+str(self.id)

class Condition(models.Model):
	condition 		= models.CharField(max_length=120, blank=True)
	condition_ru 	= models.CharField(max_length=120, blank=True)
	condition_ua 	= models.CharField(max_length=120, blank=True)
	condition_eng 	= models.CharField(max_length=120, blank=True)
	def __str__(self):
		return self.condition


class FilterUrlShortenerManager(models.Manager):
	def new_or_get(self, json_data):
		qs=self.get_queryset().filter(json_data=json_data)
		if qs.count()==1:
			new_obj = False
			url_obj=qs.first()
			shorted_slug = url_obj.shorted_slug
		else:
			new_obj = True
			url_obj=FilterUrlShortener.objects.create(json_data=json_data)
			shorted_slug = url_obj.shorted_slug
		return url_obj, new_obj

# class FilterUrlShortener(models.Model):
# 	json_data    = models.TextField(blank=False)
# 	shorted_slug = models.SlugField(default=None, unique = True, blank=True)
# 	objects      = FilterUrlShortenerManager()

# 	def __str__(self):
# 		return self.shorted_slug


# def filter_url_shortener_pre_save_reciever(sender, instance, *args, **kwargs):
# 	if not instance.shorted_slug:
# 		instance.shorted_slug = unique_slug_url_shortener_generator(instance)


# pre_save.connect(filter_url_shortener_pre_save_reciever,sender=FilterUrlShortener)


