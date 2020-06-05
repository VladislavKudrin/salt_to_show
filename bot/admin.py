from django.contrib import admin
from .models import User_telegram, LoginMode, PayMode, TelegramActivation


admin.site.register(User_telegram)
admin.site.register(LoginMode)
admin.site.register(PayMode)
admin.site.register(TelegramActivation)