from django.db import models


from imagekit import ImageSpec, register
from imagekit.processors import Transpose, Thumbnail 

class Thumbnail(ImageSpec):
    processors=[Transpose(), Thumbnail(600, 600, crop=False)]
    format='JPEG'
    options={'quality': 100}







