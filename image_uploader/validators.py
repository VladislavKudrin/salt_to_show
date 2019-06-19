import os
from django.core.exceptions import ValidationError


def validate_file_extension(value):
	ext = os.path.splitext(value.name)[1]
	print(ext)
	valid_extensions = ['.jpg']
	if not ext.lower() in valid_extensions:
		raise ValidationError(u'Unsupported file extension.')