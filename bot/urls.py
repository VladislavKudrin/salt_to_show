from django.conf.urls import url
from .views import BotView

urlpatterns = [
	url(r'^telegram/$', BotView.as_view(), name='telegram_bot'),
]