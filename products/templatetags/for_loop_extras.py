from django import template
from datetime import datetime
register = template.Library()

@register.filter
def to_none(value):
	return ""

@register.filter
def to_first(value):
	for img in value:
		if img.image_order == 1:
			final_img = img
			return img



@register.filter
def to_rus(value):
	gender_eng = ['man', 'woman', 'unisex']
	gender_rus = ['муж', 'жен', 'унисекс']
	for idx, gender in enumerate(gender_eng):
		if gender == value:
			return gender_rus[idx]
	category_eng = ['footwear', 'outwear', 'tops', 'bottoms', 'accessories']
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
	time_eng = ['minutes','minute','hours', 'hour', 'day','days', 'weeks','week']
	time_rus = ['минут','минуту','часов','час', 'день', 'дней', 'недель', 'неделю']
	for idx, time in enumerate(time_eng):
		if time in value:
			value = value.replace(time, time_rus[idx])
	return value


@register.filter
def to_ua_times(value):
	return value





