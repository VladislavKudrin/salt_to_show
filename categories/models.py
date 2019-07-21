from django.db import models
from django.db.models.signals import post_save







class Overcategory(models.Model):
	overcategory 		= models.CharField(max_length=120, blank=True)
	def __str__(self):
		return self.overcategory

class Gender(models.Model):
	gender_for 	= models.ForeignKey(Overcategory)
	gender_admin = models.CharField(max_length=120, blank=True)
	gender 		= models.CharField(max_length=120, blank=True)
	def __str__(self):
		return (self.gender)

class Category(models.Model):
	category_for 	= models.ForeignKey(Gender)
	category_admin 	= models.CharField(max_length=120, blank=True)
	category 		= models.CharField(max_length=120, blank=True)
	def __str__(self):
		return (self.category)
	
class Undercategory(models.Model):
	undercategory_for 	= models.ForeignKey(Category)
	undercategory_admin = models.CharField(max_length=120, blank=True)
	undercategory 		= models.CharField(max_length=120, blank=True)
	def __str__(self):
		return (self.undercategory)

class Size(models.Model):
	size_for 	= models.ForeignKey(Undercategory)
	size_admin 	= models.CharField(max_length=120, blank=True)
	size 		= models.CharField(max_length=120, blank=True)
	def __str__(self):
		return (self.size)

class Brand(models.Model):
	brand_name = models.CharField(max_length=120, blank=True)
	def __str__(self):
		return self.brand_name












