from django.db import models
import random
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db.models.signals import post_save

from products.models import get_filename_ext
from ecommerce.utils import random_string_generator, unique_image_id_generator



class UploadManager(models.Manager):
    def delete_uploaded_files(self, form_id):
        qs = UploadedFile.objects.filter(form_id=form_id)
        for upl_file in qs:
            upl_file.uploaded_file.delete()
            upl_file.delete()

    def compress_for_thumbnail(self, image):
        filename = image.name.split('/')[1].split('.')[0]
        first_image_pil = Image.open(image)
        im_io = BytesIO() 
        size = 250, 250
        first_image_pil.thumbnail(size)
        first_image_pil.save(im_io, first_image_pil.format , quality=70) 
        new_image = File(im_io, name=filename + '.'+first_image_pil.format)
        return new_image


    def rotate_image(self, image, rotated_x=0):
        int_rotated = int(rotated_x)
        if int_rotated != 0 or int_rotated%4 != 0:
            im = Image.open(image)
            image_rotated = im.rotate(-90*int_rotated, expand=True)
            img_io = BytesIO()
            image_rotated.save(img_io, im.format) 
            new_image = File(img_io, name='baraban')
            return new_image
        return image
        

        



def unique_form_id_generator():
    size = random.randint(10,40)
    form_id = random_string_generator(size=size)
    qs_exists = UploadedFile.objects.filter(form_id=form_id).exists()
    if qs_exists:
        return unique_form_id_generator()
    return form_id



def upload_to(instance, filename):
	new_filename = unique_image_id_generator(instance, 'uploaded_image')
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
	return "products/{final_filename}".format(
		new_filename=new_filename,
		final_filename=final_filename)

def upload_to_thumb(instance, filename):
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=name,ext=ext)
    return "temp_fotos/thumbnail/thumb_{final_filename}".format(final_filename=final_filename)



class UploadedFile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    uploaded_file = models.FileField(max_length=255, upload_to=upload_to, blank=True, null=True)
    file_id = models.CharField(max_length=40, blank=True, null=True)
    form_id = models.CharField(max_length=40, blank=True, null=True)
    # thumbnail = models.FileField(max_length=255, upload_to=upload_to_thumb, blank=True, null=True)
    objects = UploadManager()

# def uploaded_file_post_create_thumbnail(sender, created, instance, *args, **kwargs):
#     if created:
#         thumb = UploadedFile.objects.compress_for_thumbnail(instance.uploaded_file)
#         instance.thumbnail = thumb
#         instance.save()
        


# post_save.connect(uploaded_file_post_create_thumbnail, sender= UploadedFile)




