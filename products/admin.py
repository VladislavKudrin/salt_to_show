from django.contrib import admin
from django.urls import reverse
from django.conf import settings

from .models import Product, ProductImage, ProductThumbnail, ReportedProduct

class ProductImageInline(admin.TabularInline):
	model = ProductImage
	list_display = ['__str__', 'slug', 'image_order', 'image_tag']

	fields = ['image_tag', 'image','image_order', 'product']
	readonly_fields = ['image_tag', 'product']

	class Meta:
		model=ProductImage

class ProductAdmin(admin.ModelAdmin):
	list_display = ['__str__','get_absolute_url_admin', 'user', 'authentic', 'timestamp', 'slug']
	inlines = [
	ProductImageInline,
	]
	fieldsets = (
        ('Product info', {'fields': ('user', 'title', 'slug', 'description', 'price','national_shipping','condition', 'active', 'timestamp', 'currency_original', 'price_original' )}),
        ('Product brand, category and size', {'fields': ('brand','overcategory', 'sex', 'category', 'undercategory', 'size')}),
    	('Authentity', {'fields': ('authentic','get_absolute_url_admin')}),
    )


	readonly_fields = ['get_absolute_url_admin', 'timestamp']
	def get_absolute_url_admin(self, obj):
		return '<a href="{url}">Product</a>'.format(url=reverse('products:detail', kwargs={"slug":obj.slug}))


	get_absolute_url_admin.allow_tags=True
	get_absolute_url_admin.short_description = 'Product Url'
	class Meta:
		model=Product




class ProductImageAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'slug', 'image_order']

	fields = ['image_tag', 'slug', 'image_order', 'product']
	readonly_fields = ['image_tag', 'product']


	class Meta:
		model=ProductImage


admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage, ProductImageAdmin)

admin.site.register(ProductThumbnail)

admin.site.register(ReportedProduct)

