from django.contrib import admin

from .models import Product, ProductImage, ProductThumbnail, ReportedProduct

class ProductAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'slug']
	class Meta:
		model=Product

class ProductImageAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'slug', 'image_order']
	class Meta:
		model=ProductImage

admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage, ProductImageAdmin)

admin.site.register(ProductThumbnail)

admin.site.register(ReportedProduct)