from django.conf.urls import url


from .views import ThreadView, InboxView

app_name = 'chat_ecommerce'
urlpatterns = [
    url(r'^$', InboxView.as_view()),
    url(r"^(?P<username>[\w.@+-]+)", ThreadView.as_view()),
]
