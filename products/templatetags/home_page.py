from django import template
from django.conf import settings
register = template.Library()


@register.filter
def to_default_language(value):
	if type(value) != str:
		request = value
		value = value.session
		language = value.get('language')
		if language is None:
			pref = settings.DEFAULT_LANGUAGE_PREF
			value['language'] = pref
		else:
			return ''
		return request.build_absolute_uri()



@register.filter
def to_translate(value, arg):
	request = arg
	instance = value
	language = request.session.get('language')
	if language is not None:
		if instance is not None:
			return instance.return_language(language)
	return value


@register.filter
def to_user_currency(value, arg):
	request = arg
	product_price_original = value
	currency = '$'
	if product_price_original is not '':
		product_price = str(round(product_price_original)) + ' ' + currency
		if request.user.is_authenticated():
			region = request.user.region
			if region: 
				currency = region.currency
				currency_mult = region.currency_mult
				product_price = product_price_original * currency_mult
				product_price = str(round(product_price)) 
		return product_price
	return 'No price set'


