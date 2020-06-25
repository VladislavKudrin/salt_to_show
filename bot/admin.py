from django.contrib import admin
from .models import User_telegram, LoginMode, PayMode, TelegramActivation, ChannelProductMessage



class TelegramActivationAdmin(admin.ModelAdmin):

	fields = ['email', 'chat_id', 'key', 'activated', 'timestamp', 'update']
	readonly_fields=['timestamp', 'update']


	class Meta:
		model=TelegramActivation

admin.site.register(User_telegram)
admin.site.register(LoginMode)
admin.site.register(PayMode)
admin.site.register(TelegramActivation, TelegramActivationAdmin)
admin.site.register(ChannelProductMessage)