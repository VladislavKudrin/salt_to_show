from django import template
from datetime import datetime
from django.conf import settings
from django.shortcuts import redirect
register = template.Library()



@register.filter
def get_chat_options(value):
	if settings.CHAT_WITH_PRODUCTS:
		return settings.CHAT_WITH_PRODUCTS
	else:
		return False


@register.filter
def to_next_path(value):
	if '?' in value:
		link = value.split('?')[1]
		link = '?' + link
		return link 	
	return ''
@register.filter
def to_clean_path(value):
	print(value[3:])
	return value

@register.filter
def index(array, index):
	print(array)
	return ''

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
def to_none(value):
	return ""

@register.filter
def to_first(value):
	for img in value:
		if img.image_order == 1:
			final_img = img
			return final_img





@register.filter
def to_rus(value):
	gender_eng = ['man', 'woman', 'unisex']
	gender_rus = ['мужское', 'женское', 'унисекс']
	for idx, gender in enumerate(gender_eng):
		if gender == value:
			return gender_rus[idx]
	category_eng = ['footwear', 'outerwear', 'tops', 'bottoms', 'accessories']
	category_rus = ['обувь', 'верхняя одежда', 'верх', 'низ', 'аксессуары']
	for idx, category in enumerate(category_eng):
		if category == value:
			return category_rus[idx]



@register.filter
def to_ua(value):
	return value

@register.filter
def to_rus_times(value):
	month_eng = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
	month_rus = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
	for idx, month in enumerate(month_eng):
		if month == value.split(' ')[0]:
			value = value.replace(value.split(' ')[0], month_rus[idx])
			print(value)
			return value
	time_eng = ['minutes','minute','hours', 'hour', 'days','day', 'weeks','week']
	time_rus = ['мин.','минуту','часов', 'час', 'дней', 'день','недель', 'неделю']
	for idx, time in enumerate(time_eng):
		if time in value:
			value = value.replace(time, time_rus[idx])
	return value


@register.filter
def to_ua_times(value):
	month_eng = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
	month_ua = ['Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень', 'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень']
	for idx, month in enumerate(month_eng):
		if month == value.split(' ')[0]:
			value = value.replace(value.split(' ')[0], month_ua[idx])
			print(value)
			return value
	time_eng = ['minutes','minute','hours', 'hour', 'days','day', 'weeks','week']
	time_ua = ['хв.','хвилину','годин', 'година', 'днів', 'день','тижнів', 'тиждень']
	for idx, time in enumerate(time_eng):
		if time in value:
			value = value.replace(time, time_ua[idx])
	return value

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
	product = value
	product_price = product.price
	currency = ' $'
	product_price = str(round(product_price)) + ' ' + currency
	if request.user.is_authenticated():
		region = request.user.region
		if region: 
			currency = region.currency
			currency_mult = region.currency_mult
			product_price = product.price * currency_mult
			product_price = str(round(product_price)) + ' ' + currency
	return product_price





