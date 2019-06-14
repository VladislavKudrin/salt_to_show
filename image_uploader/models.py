from django.db import models
import random




from ecommerce.utils import random_string_generator





def unique_form_id_generator():
    size = random.randint(10,40)
    form_id = random_string_generator(size=size)
    qs_exists = UploadedFile.objects.filter(form_id=form_id).exists()
    if qs_exists:
        return unique_form_id_generator()
    return form_id



def upload_to(instance, filename):
	new_filename = random.randint(1,31231231)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
	return "temp_fotos/{new_filename}/{final_filename}".format(
		new_filename=new_filename,
		final_filename=final_filename)




class UploadedFile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    uploaded_file = models.FileField(max_length=255, upload_to=upload_to)
    original_filename = models.CharField(max_length=255)
    file_id = models.CharField(max_length=40)
    form_id = models.CharField(max_length=40)