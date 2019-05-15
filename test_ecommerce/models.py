
import six

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class Example(models.Model):
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)

    title = models.CharField(max_length=255)
    input_file = models.FileField(max_length=255, upload_to='example', storage=fs)


class Example2(models.Model):
    title = models.CharField(max_length=255)


@six.python_2_unicode_compatible
class ExampleFile(models.Model):
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)

    example = models.ForeignKey(Example2, related_name='files', on_delete=models.CASCADE)
    input_file = models.FileField(max_length=255, upload_to='example', storage=fs)

    def __str__(self):
        return six.text_type(self.input_file)

























# from django.db import models
# import random 
# import os
# # Create your models here.
# def get_filename_ext(filepath):
# 	base_name = os.path.basename(filepath)
# 	name, ext = os.path.splitext(base_name)
# 	return name, ext


# def upload_image_path(instance, filename):
# 	print(instance)
# 	print(filename)
# 	new_filename = random.randint(1,31231231)
# 	name, ext = get_filename_ext(filename)
# 	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
# 	return "products/{new_filename}/{final_filename}".format(
# 		new_filename=new_filename,
# 		final_filename=final_filename)

# class TestModel(models.Model):
# 	username 		= models.CharField(max_length=255, blank=True, null=True)
# 	email 			= models.EmailField(max_length=255, blank=True)
# 	full_name 		= models.CharField(max_length=255, blank=True, null=True)
# 	image			= models.ImageField(upload_to=upload_image_path, null=True, blank=True)
