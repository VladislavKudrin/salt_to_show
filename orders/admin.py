from django.contrib import admin

from .models import Order, Transaction, Payout

from django.urls import reverse
from django.conf import settings

# from .models import Product, ProductImage, ProductThumbnail, ReportedProduct

# class ProductImageInline(admin.TabularInline):
# 	model = ProductImage
# 	list_display = ['__str__', 'slug', 'image_order', 'image_tag']

# 	fields = ['image_tag', 'image','image_order', 'product']
# 	readonly_fields = ['image_tag', 'product']

# 	class Meta:
# 		model=ProductImage

# class ProductAdmin(admin.ModelAdmin):
# 	list_display = ['__str__','get_absolute_url_admin', 'user', 'authentic', 'timestamp', 'slug', 'price']
# 	inlines = [
# 	ProductImageInline,
# 	]
# 	fieldsets = (
#         ('Product info', {'fields': ('user', 'title', 'slug', 'description', 'price','national_shipping','condition', 'active', 'timestamp', 'currency_original', 'price_original' )}),
#         ('Product brand, category and size', {'fields': ('brand','overcategory', 'sex', 'category', 'undercategory', 'size')}),
#     	('Authentity', {'fields': ('authentic','get_absolute_url_admin')}),
#     )


# 	readonly_fields = ['get_absolute_url_admin', 'timestamp']
# 	def get_absolute_url_admin(self, obj):
# 		return '<a href="{url}">Product</a>'.format(url=reverse('products:detail', kwargs={"slug":obj.slug}))


# 	get_absolute_url_admin.allow_tags=True
# 	get_absolute_url_admin.short_description = 'Product Url'
# 	class Meta:
# 		model=Product


class OrderAdmin(admin.ModelAdmin):
	list_display = [
	'order_id', 'timestamp', 'status', 'buyer_link', 
	'seller_link', 'product', 'track_number','total', 
	]


	fieldsets = (
        ('Order info', {'fields':(	
			'order_id', 'status',  'timestamp', 'updated', 
			'billing_profile',
			'buyer_link',
			 'seller_link', 
			 'product', 
			 'product_link',
			 'total',
			 'shipping_address_final', 
			 'track_number',
			 'feedback', 
			 'active',  
			 
	  )}),
    )

	readonly_fields = ['timestamp', 'updated', 'product_link', 'buyer_link', 'seller_link']

	def product_link(self, obj):
		return '<a href="{url}">Product</a>'.format(url=reverse('products:detail', kwargs={"slug":obj.product.slug}))

	def buyer_link(self, obj):
		return '<a href="{url}">Buyer profile</a>'.format(url=reverse('profile', kwargs={"username":obj.billing_profile.user.username}))

	def seller_link(self, obj):
		return '<a href="{url}">Seller profile</a>'.format(url=reverse('profile', kwargs={"username":obj.product.user.username}))

	product_link.allow_tags = True
	buyer_link.allow_tags = True
	seller_link.allow_tags =True

admin.site.register(Order, OrderAdmin)





admin.site.register(Transaction)




class PayoutAdmin(admin.ModelAdmin):
    list_display = ('order', 'to_billing_profile', 'successful', 'timestamp')
    list_filter = ('successful',)
    search_fields = ('order', 'to_billing_profile')
    ordering = ('timestamp',)
    filter_horizontal = ()


admin.site.register(Payout, PayoutAdmin)