# from django.contrib import admin


# from .models import Thread, ChatMessage

# class ChatMessage(admin.TabularInline):
#     model = ChatMessage

# class ThreadAdmin(admin.ModelAdmin):
#     inlines = [ChatMessage]
#     class Meta:
#         model = Thread 


# admin.site.register(Thread, ThreadAdmin)




# # from django.contrib import admin

# # from .models import Dialog, Message


# # class DialogAdmin(admin.ModelAdmin):
# #     list_display = ('id', 'created', 'modified', 'owner', 'opponent')
# #     list_filter = ('created', 'modified', 'owner', 'opponent')


# # admin.site.register(Dialog, DialogAdmin)


# # class MessageAdmin(admin.ModelAdmin):
# #     list_display = (
# #         'id',
# #         'created',
# #         'modified',
# #         'is_removed',
# #         'dialog',
# #         'sender',
# #         'text',
# #     )
# #     list_filter = ('created', 'modified', 'is_removed', 'dialog', 'sender')


# # admin.site.register(Message, MessageAdmin)
