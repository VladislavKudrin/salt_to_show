from django.db import models
from django.db.models.signals import post_save



class Size(models.Model):
	size_for 	= models.CharField(max_length=120, blank=True)
	size 		= models.CharField(max_length=120, blank=True)
	def __str__(self):
		return self.size


# class Size(models.Model):
# 	size_pants  		 = models.CharField(max_length=120, blank=True)
# 	size_shoes 			 = models.CharField(max_length=120, blank=True)
# 	size_tops 			 = models.CharField(max_length=120, blank=True)
# 	def __str__(self):
# 		if self.size_pants:
# 			name = self.size_pants.replace('Pants/', '')
# 			return name		
# 		if self.size_shoes:
# 			name = self.size_shoes.replace('Shoes/', '')
# 			return name
# 		if self.size_tops:
# 			name = self.size_tops.replace('Tops/', '')
# 			return name


# def post_save_create_size_reciever(sender, instance, created, *args, **kwargs):
# 	if created:
# 		if instance.size_shoes:
# 			instance.size_shoes = 'Shoes/' + instance.size_shoes
# 			instance.save()
# 		if instance.size_pants:
# 			instance.size_pants = 'Pants/' + instance.size_pants
# 			instance.save()
# 		if instance.size_tops:
# 			instance.size_tops = 'Tops/' + instance.size_tops
# 			instance.save()

# post_save.connect(post_save_create_size_reciever, sender=Size)









