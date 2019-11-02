import random
import string
import os
from .settings import BASE_DIR
from categories.models import Brand
from django.utils.text import slugify


def random_string_generator_username():
    return str(random.randint(0, 99))

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



def unique_key_generator(instance):
    """
    This is for a Django project with order id field.
    """
    size = random.randint(30,45)
    key = random_string_generator(size=size)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key


def unique_order_id_generator(instance):
    """
    This is for a Django project with order id field.
    """
    order_new_id = random_string_generator()
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return order_new_id


def unique_image_id_generator(instance, image_type):
    size = random.randint(30,45)
    key = random_string_generator(size=size)
    Klass = instance.__class__
    if image_type == 'uploaded_image':
        qs_exists = Klass.objects.filter(uploaded_file=key).exists()
    else:
        qs_exists = Klass.objects.filter(unique_image_id=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key



def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)[:50] # takes only first 50 from what slugify returns
        if slug == '':
            slug = random_string_generator(size=random.randint(3, 5))[:50]
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        slug = slug[:-5] # removes last 5 chars from existing slug
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4) #adds new random 5 chars
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug







# def create_brands(f):
# #     # print(f.read())
#     brand_list = []
#     for i in f:
#         i = i.rstrip()
#         brand_list.append(i)
#         Brand.objects.create(brand_name=i)
#         print(i)
#     return brand_list

# path = os.path.join(BASE_DIR, 'brandsS.txt')
# f = open(path, "r")
   
# brand_list = create_brands(f)


