import random
import string


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_url_shortener_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        size = random.randint(10,11)
        slug = random_string_generator(size=size)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(shorted_slug=slug).exists()
    if qs_exists:
        slug = slug[:-5]
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4) #adds new random 5 chars
                )
        return unique_slug_url_shortener_generator(instance, new_slug=new_slug)
    return slug


def link_to_data(link):
    linked_data = {}
    if linked_data is None:
        print('wdawdawdawd')
    if link is not None:
        words = link.split('&')
        data_brand_link=None
        data_price_link=None
        data_overcategory_link=None
        data_gender_link=None
        data_category_link=None
        data_undercategory_link=None
        data_size_link=None
        data_condition_link=None
        for word in words:
                type_ = word.split('=')
                if type_[0] == 'overcategory':
                    data_overcategory_link = type_[1]
                    if '/' in data_overcategory_link:
                        data_overcategory_link= data_overcategory_link.replace('/', '')
                    linked_data['overcategory'] = data_overcategory_link
                if type_[0] == 'gender':
                    data_gender_link = type_[1]
                    if '/' in data_gender_link:
                        data_gender_link= data_gender_link.replace('/', '')
                    linked_data['gender'] = data_gender_link
                if type_[0] == 'category':
                    data_category_link = type_[1].split('+')
                    if '/' in data_category_link:
                        data_category_link= data_category_link.replace('/', '')
                    linked_data['category'] = data_category_link
                if type_[0] == 'undercategory':
                    data_undercategory_link = type_[1].split('+')
                    if '/' in data_undercategory_link:
                        data_undercategory_link= data_undercategory_link.replace('/', '')
                    linked_data['undercategory'] = data_undercategory_link
                if type_[0] == 'size':
                    data_size_link = type_[1].split('+')
                    if '/' in data_size_link:
                        data_size_link= data_size_link.replace('/', '')
                    linked_data['size'] = data_size_link
                if type_[0] == 'price':
                    data_price_link = type_[1].split('+')
                    if '/' in data_price_link:
                        data_price_link= data_price_link.replace('/', '')
                    linked_data['price'] = data_price_link
                if type_[0] == 'condition':
                    data_condition_link = type_[1].split('+')
                    if '/' in data_condition_link:
                        data_condition_link= data_condition_link.replace('/', '')
                    linked_data['condition'] = data_condition_link
                if type_[0] == 'brand':
                    data_brand_link = type_[1].split('+')
                    if '/' in data_brand_link:
                        data_brand_link= data_brand_link.replace('/', '')
                    linked_data['brand'] = data_brand_link
    if len(linked_data) == 0:
        linked_data = 'all'
    return linked_data




def build_link_categories(request):
    link_codiert = ''
    data_overcategory = request.GET.get('overcategory')
    data_gender = request.GET.get('gender')
    data_category = request.GET.getlist('category')
    data_undercategory = request.GET.getlist('undercategory')
    data_brand = request.GET.getlist('brand')
    data_price = request.GET.getlist('price')
    data_size = request.GET.getlist('size')
    data_condition = request.GET.getlist('condition')
    data_sort = request.GET.get('sort')
    if data_undercategory:
        link_codiert=link_codiert+"undercategory="
        for id_ in data_undercategory:
            if id_== data_undercategory[-1]:
                link_codiert = link_codiert + "{id}".format(id=int(id_))+'&'
            else:
                link_codiert = link_codiert + "{id}".format(id=int(id_))+'+'
    if data_gender:
        link_codiert=link_codiert+"gender="
        for id_ in data_gender:
            if id_== data_gender[-1]:
                link_codiert = link_codiert + "{id}".format(id=int(id_))+'&'
            else:
                link_codiert = link_codiert + "{id}".format(id=int(id_))+'+'
    if data_overcategory:
        link_codiert=link_codiert+"overcategory="
        for id_ in data_overcategory:
            if id_== data_overcategory[-1]:
                link_codiert = link_codiert + "{id}".format(id=int(id_))+'&'
            else:
                link_codiert = link_codiert + "{id}".format(id=int(id_))+'+'
    if data_size:
        link_codiert=link_codiert+"size="
        for id_ in data_size:
            if id_== data_size[-1]:
                link_codiert = link_codiert + "{id}".format(id=int(id_))+'&'
            else:
                link_codiert = link_codiert + "{id}".format(id=int(id_))+'+'
    if data_brand:
        link_codiert=link_codiert+"brand="
        for id_ in data_brand:
            if id_== data_brand[-1]:
                link_codiert = link_codiert + "{id}".format(id=int(id_))+'&'
            else:
                link_codiert = link_codiert + "{id}".format(id=int(id_))+'+'
    if data_condition:
        link_codiert=link_codiert+"condition="
        for id_ in data_condition:
            if id_== data_condition[-1]:
                link_codiert = link_codiert + "{id}".format(id=int(id_))+'&'
            else:
                link_codiert = link_codiert + "{id}".format(id=int(id_))+'+'
    if data_price:
        price_min = data_price[0]
        price_max = data_price[1]
        if not price_min and price_max:
            link_codiert = link_codiert + "price=+{price}".format(price=data_price[1])+'&'
        elif not price_max and price_min:
            link_codiert = link_codiert + "price={price}+".format(price=data_price[0])+'&'
        elif price_max and price_min:
            link_codiert = link_codiert + "price={price_min}+{price_max}".format(price_min=data_price[0], price_max=data_price[1])+'&'
    return link_codiert


