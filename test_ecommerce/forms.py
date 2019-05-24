
from django.urls import reverse

import django_bootstrap3_form

from django_file_form.forms import UploadedFileField, MultipleUploadedFileField, FileFormMixin

from .models import Example, Example2, ExampleFile


class BaseForm(FileFormMixin, django_bootstrap3_form.BootstrapForm):
    title = django_bootstrap3_form.CharField()


class ExampleForm(BaseForm):
    prefix = 'example'
    input_file = UploadedFileField()

    def save(self):
        Example.objects.create(
            title=self.cleaned_data['title'],
            input_file=self.cleaned_data['input_file']
        )
        self.delete_temporary_files()


class MultipleFileExampleForm(BaseForm):
    prefix = 'example'
    input_file = MultipleUploadedFileField()

    def save(self):
        example = Example2.objects.create(
            title=self.cleaned_data['title']
        )

        for f in self.cleaned_data['input_file']:
            ExampleFile.objects.create(
                example=example,
                input_file=f
            )

        self.delete_temporary_files()


class ExistingFileForm(ExampleForm):
    prefix = 'example'

    def get_upload_url(self):
        return reverse('test:example_handle_upload')


















# from django import forms
# from .models import TestModel
# from PIL import Image
# from io import BytesIO
# from django.core.files.base import ContentFile
# from django_file_form.forms import FileFormMixin, UploadedFileField
# class TestModelForm(FileFormMixin, forms.ModelForm):
# 	input_file = UploadedFileField()
# 	class Meta:
# 		model = TestModel
# 		fields=[
# 			'username',
# 			'email',
# 			'full_name',
# 		]

	# def clean_username(self):
	# 	data = self.cleaned_data
	# 	username = data.get('username')
	# 	if username == 'abc':
	# 		self.add_error('username', "Please specify time at address if less than 3 years.")
	# 	return username

	# def clean_image(self):
	# 	data = self.cleaned_data
	# 	im = Image.open(data.get('image'))
	# 	thumb_io = BytesIO()
	# 	im.save(thumb_io, im.format)

	# 	im.verify()
	# 	# image.verify()
	# 	return data.get('image')

