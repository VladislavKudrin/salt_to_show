from django.conf.urls import url
from .views import BotView, delete_activation_key_view

urlpatterns = [
	url(r'^telegram/$', BotView.as_view(), name='telegram_bot'),
	url(r'^delete_activation/$', delete_activation_key_view, name='delete_activation_key'),
]