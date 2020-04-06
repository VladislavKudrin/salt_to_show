from django.core.files import File
from io import BytesIO
from PIL import Image




def rotate_image(image=None, rotated_x=0):
		if rotated_x:
			int_rotated = int(rotated_x)
			if int_rotated != 0 or int_rotated%4 != 0:
				with Image.open(image) as im:
					image_rotated = im.rotate(-90*int_rotated, expand=True)
					img_io = BytesIO()
					image_rotated.save(img_io, im.format)
					image = File(img_io, name=str(image))
		return image





