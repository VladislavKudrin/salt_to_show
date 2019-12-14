from django.contrib import admin
from django.urls import reverse
from django.conf import settings

from .models import Product, ProductImage, ProductThumbnail, ReportedProduct


class ProductAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'user', 'authentic', 'timestamp', 'slug']
	fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Authentity', {'fields': ('authentic','get_absolute_url_admin')}),
        ('Product info', {'fields': ('title', 'slug', 'description', 'price', 'active', 'timestamp')}),
        ('Product brand, category and size', {'fields': ('brand','overcategory', 'sex', 'category', 'undercategory', 'size')}),
        ('Condition', {'fields': ('condition',)}),
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
	class Meta:
		model=ProductImage

admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage, ProductImageAdmin)

admin.site.register(ProductThumbnail)

admin.site.register(ReportedProduct)