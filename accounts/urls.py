from django.conf.urls import url


from products.views import UserProductHistoryView
from .views import (
	AccountHomeView,
	AccountEmailActivateView,
	UserDetailUpdateView,
    ProfileView,
    WishListView,
    wishlistupdate,
    languge_pref_view
    )



urlpatterns = [
    url(r'^$',AccountHomeView.as_view(), name='home'),
    url(r'^language/$',languge_pref_view, name='language-pref'),
    url(r'^wish-list/$', WishListView.as_view(), name='wish-list'),
    url(r'^wishlist-update/$', wishlistupdate, name='wish-list-update'),
    url(r'^history/products/$',UserProductHistoryView.as_view(), name='history-product'),
    url(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$',
    	AccountEmailActivateView.as_view(), name='email-activate'),
    url(r'^email/resend-activation/$',
    	AccountEmailActivateView.as_view(), name='resend-activation'),
    url(r'^details/$',UserDetailUpdateView.as_view(), name='user-update'),    
    url(r'^profile/(?P<username>[\w.@+-]+)/$', ProfileView.as_view(), name='profile'),

]



