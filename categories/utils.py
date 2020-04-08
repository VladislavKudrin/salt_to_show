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