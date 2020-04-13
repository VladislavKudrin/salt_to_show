from django import template
from django.conf import settings
from accounts.models import Region


register = template.Library()

@register.filter
def to_user_currency(value, arg):
	request = arg
	product_price_original = value
	default_currency = settings.DEFAULT_CURRENCY
	default_region = Region.objects.filter(currency=default_currency)
	if product_price_original is not '':
		product_price = str(round(product_price_original)) + ' $'
		if request.user.is_authenticated():
			region = request.user.region
			if region: 
				currency = region.currency
				currency_mult = region.currency_mult
				product_price = product_price_original * currency_mult
				product_price = str(round(product_price)) + ' ' + currency
		else:
			if default_region.exists():
				currency = default_region.first().currency
				currency_mult = default_region.first().currency_mult
				product_price = product_price_original * currency_mult
				product_price = str(round(product_price)) + ' ' + currency
		return product_price
	return 'No price set'
