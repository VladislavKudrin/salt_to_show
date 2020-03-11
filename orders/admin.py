from django.contrib import admin

from .models import Order, Transaction, Payout

admin.site.register(Order)

admin.site.register(Transaction)




class PayoutAdmin(admin.ModelAdmin):
    list_display = ('order', 'to_billing_profile', 'successful', 'timestamp')
    list_filter = ('successful',)
    search_fields = ('order', 'to_billing_profile')
    ordering = ('timestamp',)
    filter_horizontal = ()


admin.site.register(Payout, PayoutAdmin)