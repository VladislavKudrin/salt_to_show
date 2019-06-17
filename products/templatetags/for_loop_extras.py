from django import template

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