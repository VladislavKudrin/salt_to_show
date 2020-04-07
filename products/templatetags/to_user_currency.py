from django import template
register = template.Library()

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
				product_price = str(round(product_price)) + ' ' + currency

		return product_price
	return 'No price set'