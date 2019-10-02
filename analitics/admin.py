from django.contrib import admin

from .models import ObjectViewed, UserSession

class UserSessionAdmin(admin.ModelAdmin):
	list_display = ['user', 'active', 'ended']
	list_filter = ('active', 'ended')
	search_fields = ('user__email',)
	class Meta:
		model=UserSession


admin.site.register(ObjectViewed)
admin.site.register(UserSession, UserSessionAdmin)

