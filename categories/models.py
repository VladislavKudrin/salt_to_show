from django.db import models
from django.db.models.signals import post_save







class Overcategory(models.Model):
	overcategory 		= models.CharField(max_length=120, blank=True)
	overcategory_ru 	= models.CharField(max_length=120, blank=True)
	overcategory_eng 	= models.CharField(max_length=120, blank=True)
	overcategory_ua 	= models.CharField(max_length=120, blank=True)
	def __str__(self):
		return self.overcategory

class Gender(models.Model):
	gender_for 	= models.ForeignKey(Overcategory)
	gender_admin = models.CharField(max_length=120, blank=True)
	gender 		= models.CharField(max_length=120, blank=True)
	gender_ru 	= models.CharField(max_length=120, blank=True)
	gender_eng 	= models.CharField(max_length=120, blank=True)
	gender_ua 	= models.CharField(max_length=120, blank=True)
	def __str__(self):
		return (self.gender)

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

class Size(models.Model):
	size_for 		= models.CharField(max_length=120, blank=True)
	size_admin 		= models.CharField(max_length=120, blank=True)
	size 			= models.CharField(max_length=120, blank=True)
	size_kids 		= models.CharField(max_length=120, blank=True)
	def __str__(self):
		return (self.size + '_' + self.size_kids)

class Brand(models.Model):
	brand_name = models.CharField(max_length=120, blank=True)
	def __str__(self):
		return self.brand_name

class Condition(models.Model):
	condition 		= models.CharField(max_length=120, blank=True)
	condition_ru 	= models.CharField(max_length=120, blank=True)
	condition_ua 	= models.CharField(max_length=120, blank=True)
	condition_eng 	= models.CharField(max_length=120, blank=True)
	def __str__(self):
		return self.condition







