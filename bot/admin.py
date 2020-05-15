from django.contrib import admin
from .models import User_telegram, LoginMode, PayMode


admin.site.register(User_telegram)
admin.site.register(LoginMode)
admin.site.register(PayMode)