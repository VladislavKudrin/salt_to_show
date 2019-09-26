from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse






class Overcategory(models.Model):
	overcategory 		= models.CharField(max_length=120, blank=True)
	overcategory_ru 	= models.CharField(max_length=120, blank=True)
	overcategory_eng 	= models.CharField(max_length=120, blank=True)
	overcategory_ua 	= models.CharField(max_length=120, blank=True)
	def __str__(self):
		return self.overcategory
	def return_language(self, language):
		if language == 'RU':
			return self.overcategory_ru
		elif language == 'EN':
			return self.overcategory_eng
		elif language == 'UA':
			return self.overcategory_ua
		else:
			return self.overcategory_eng
		return self
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
	def return_language(self, language):
		if language == 'RU':
			return self.gender_ru
		elif language == 'EN':
			return self.gender_eng
		elif language == 'UA':
			return self.gender_ua
		else:
			return self.gender_eng
		return self
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
	def return_language(self, language):
		if language == 'RU':
			return self.category_ru
		elif language == 'EN':
			return self.category_eng
		elif language == 'UA':
			return self.category_ua
		else:
			return self.category_eng
		return self
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
	def return_language(self, language):
		if language == 'RU':
			return self.undercategory_ru
		elif language == 'EN':
			return self.undercategory_eng
		elif language == 'UA':
			return self.undercategory_ua
		else:
			return self.undercategory_eng
		return self
	def get_absolute_url(self):
		return reverse('products:list') + 'overcategory='+str(self.undercategory_for.category_for.gender_for.id) + '&gender='+str(self.undercategory_for.category_for.id) + '&undercategory='+str(self.id)
class Size(models.Model):
	size_for 		= models.CharField(max_length=120, blank=True)
	size_admin 		= models.CharField(max_length=120, blank=True)
	size 			= models.CharField(max_length=120, blank=True)
	size_kids 		= models.CharField(max_length=120, blank=True)
	size_type 		= models.ForeignKey(Overcategory, blank = True, null=True)
	def __str__(self):
		return (self.size + '_'+self.size_for+'_'+self.size_type.overcategory)

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
	def return_language(self, language):
		if language == 'RU':
			return self.condition_ru
		elif language == 'EN':
			return self.condition_eng
		elif language == 'UA':
			return self.condition_ua
		else:
			return self.condition_eng
		return self







