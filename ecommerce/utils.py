import random
import string
import os
from .settings import BASE_DIR
from categories.models import Brand
from django.utils.text import slugify
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from django.contrib import messages
import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files import File
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.shortcuts import render



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



def add_message(backend, user, request, response, *args, **kwargs):
    messages.add_message(request, messages.SUCCESS, _("You're in"))


alphanumeric = RegexValidator(r'^[0-9a-zA-Z_.-]+$', _('Only alphanumeric characters are allowed'))
alphaSpaces = RegexValidator(r'^[a-zA-Zа-яА-ЯҐЄІЇґєії\'\`\’\-\. ]+$', 'Only letters and spaces are allowed')
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'")


def get_data_from_novaposhta_api():
    print('Function call from cron job')
    r = requests.post('http://testapi.novaposhta.ua/v2.0/json/AddressGeneral/getWarehouses', json={
        "modelName": "AddressGeneral",
        "calledMethod": "getWarehouses",
        "methodProperties": {
        "Language": "ru",
        },
        "apiKey": "f5c686be4fb428d1b7c3aa4fb730496b"
          }
        )

    data = r.json()['data']
    offices_ua = []
    offices_ru = []
    for i in data: 
        number = i['Number']
        address_ua = i['ShortAddress']
        address_ru = i['ShortAddressRu']

        string_ua = f'Відділення № {number}, {address_ua}'
        offices_ua.append(string_ua)

        string_ru = f'Отделение № {number}, {address_ru}'
        offices_ru.append(string_ru)

    path_ua = os.path.join(BASE_DIR, "static_my_project", 'post_offices_ua.txt')
    with open(path_ua, 'w') as f:
        myfile = File(f)
        for listitem in offices_ua:
            f.write('%s\n' % listitem)
    myfile.closed
    f.closed

    path_ru = os.path.join(BASE_DIR, "static_my_project", 'post_offices_ru.txt')
    with open(path_ru, 'w') as f:
        myfile = File(f)
        for listitem in offices_ru:
            f.write('%s\n' % listitem)
    myfile.closed
    f.closed

    print(f'Offices_ua written, Offices_ru written')
    return 

def stay_where_you_are(request):
    prev_url = request.META.get('HTTP_REFERER')
    if prev_url is not None: 
        return redirect(prev_url)
    else:
        return redirect('/')



def my_render(request, *args, **kwargs):
    template_location = args[0]
    args_list = list(args)
    if request.user_agent.is_mobile:
        args_list[0] = 'mobile/' + template_location
        args = tuple(args_list)
        return render(request, *args, **kwargs)
    else:
        args_list[0] = 'desktop/' + template_location
        args = tuple(args_list)
        return render(request, *args, **kwargs)
 

 # def my_render(request, *args, **kwargs):
 #    template_location = args[0]
 #    args_list = list(args)

 #    if request.user_agent.is_mobile:
 #        args_list[0] = 'mobile/' + template_location
 #        args_list[1] = args_list[1]
 #        args_list = args_list[:-1] # remove not needed context
 #        args = tuple(args_list)
 #        return render(request, *args, **kwargs)

 #    else:
 #        args_list[0] = 'desktop/' + template_location
 #        args_list[1] = args_list[2]
 #        args_list = args_list[:-1] # remove not needed context
 #        args = tuple(args_list)
 #        return render(request, *args, **kwargs)

               
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


