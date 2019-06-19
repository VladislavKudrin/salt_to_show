from django.contrib import admin

from .models import Product, ProductImage, ImageOrderUtil

class ProductAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'slug']
	class Meta:
		model=Product

admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage)

admin.site.register(ImageOrderUtil)
