from django.contrib import admin
from .models import BillingProfile, Card, Charge, Feedback


admin.site.register(BillingProfile)

admin.site.register(Card)

admin.site.register(Feedback)



# admin.site.register(Charge)