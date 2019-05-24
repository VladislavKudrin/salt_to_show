from django.db import models
from django.db.models.signals import post_save



class Size(models.Model):
	size_for 	= models.CharField(max_length=120, blank=True)
	size 		= models.CharField(max_length=120, blank=True)
	def __str__(self):
		return self.size



class Brand(models.Model):
	brand_name = models.CharField(max_length=120, blank=True)
	def __str__(self):
		return self.brand_name






