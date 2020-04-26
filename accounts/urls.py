from django.conf.urls import url
from django.views.generic import RedirectView
from products.views import UserProductHistoryView
from .views import *




urlpatterns = [
    url(r'^$',RedirectView.as_view(url='/products'), name='home'),
    url(r'^language/$',languge_pref_view, name='language-pref'),
    url(r'^wish-list/$', WishListView.as_view(), name='wish-list'),
    url(r'^wishlist-update/$', wishlistupdate, name='wish-list-update'),
    url(r'^history/products/$',UserProductHistoryView.as_view(), name='history-product'),
    url(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', AccountEmailActivateView.as_view(), name='email-activate'),
    url(r'^email/resend-activation/$', AccountEmailActivateView.as_view(), name='resend-activation'),  
    url(r'^details/$',AccountUpdateView.as_view(), name='user-update'), 
]








