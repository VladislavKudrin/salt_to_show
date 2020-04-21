from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models


from .models import Thread, ChatMessage, Notification

class ChatMessage(admin.TabularInline):
	model = ChatMessage
	fields = ('thread', 'user','message','timestamp' )
	extra = 0
	formfield_overrides = {
	models.CharField: {'widget': TextInput(attrs={'size':'20'})},
	models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':40})},
	}
	readonly_fields = ['timestamp']


class ThreadAdmin(admin.ModelAdmin):
	list_display = ['id', 'first', 'second','timestamp', 'product']
	inlines = [ChatMessage]
	class Meta:
		model = Thread


	readonly_fields = ['timestamp']

admin.site.register(Thread, ThreadAdmin)

admin.site.register(Notification)


