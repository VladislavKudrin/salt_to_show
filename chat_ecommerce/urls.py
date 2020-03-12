from django.conf.urls import url


from .views import ThreadView, InboxView,set_chat_timezone


urlpatterns = [
    url(r'^$', InboxView.as_view(), name='inbox'),
    url(r'set_chat_timezone/$', ThreadView.as_view(), name='timezone'),
    url(r'^(?P<username>[\w.@+-]+)/$', ThreadView.as_view(), name='chat-thread'),
    url(r'^(?P<username>[\w.@+-]+)/(?P<product_id>[\w.@+-]+)/$', ThreadView.as_view(), name='chat-thread-product'),

]
