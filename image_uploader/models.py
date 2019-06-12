# from django.db import models

# def upload_to(instance, filename):
# 	new_filename = random.randint(1,31231231)
# 	name, ext = get_filename_ext(filename)
# 	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
# 	return "temp_fotos/{new_filename}/{final_filename}".format(
# 		new_filename=new_filename,
# 		final_filename=final_filename)
# class UploadedFile(models.Model):
#     created = models.DateTimeField(default=timezone.now)
#     uploaded_file = models.FileField(max_length=255, upload_to=upload_to)
#     original_filename = models.CharField(max_length=255)
#     field_name = models.CharField(max_length=255, null=True, blank=True)
#     file_id = models.CharField(max_length=40)
#     form_id = models.CharField(max_length=40)