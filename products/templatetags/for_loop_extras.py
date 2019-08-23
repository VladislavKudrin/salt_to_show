from django import template
from datetime import datetime
from django.conf import settings

register = template.Library()

@register.filter
def index(array, index):
	print(array)
	return ''

@register.filter
def to_default_language(value):
	language = value.get('language')
	if language is None:
		pref = settings.DEFAULT_LANGUAGE_PREF
		value['language'] = pref
	else:
		return ''
	return ''

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
	time_rus = ['минут','минуту','часов', 'час', 'дней', 'день','недель', 'неделю']
	for idx, time in enumerate(time_eng):
		if time in value:
			value = value.replace(time, time_rus[idx])
	return value


@register.filter
def to_ua_times(value):
	return value




