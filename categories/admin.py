from django.contrib import admin

from .models import Size

class SizeAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'size_for']
	class Meta:
		model=Size


admin.site.register(Size, SizeAdmin)
