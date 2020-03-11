from django.conf.urls import url

from billing.views import PayView, PayCallbackView, PayToUserView, PayToUserCallbackView
from .tests import response_test


urlpatterns = [
    url(r'^pay/$', PayView.as_view(), name='pay_view'),
    url(r'^pay-callback/$', PayCallbackView.as_view(), name='pay_callback'),
    url(r'^pay2user-callback/$', PayToUserCallbackView.as_view(), name='pay2user_callback'),
    url(r'^test/$', response_test, name='test_resp'),
    url(r'^pay2user/(?P<secret_key>[\w.@+-=&]+)$', PayToUserView.as_view(), name='pay2user'),
]