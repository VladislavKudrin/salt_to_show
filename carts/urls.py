from django.conf.urls import url



from .views import (
    cart_update,
    cart_home,
    checkout_home,
    checkout_done_view

    )



urlpatterns = [
    url(r'^$',cart_home, name='home'),
	url(r'^checkout/$', checkout_home, name='checkout'),
    url(r'^update/$', cart_update, name='update'),
    url(r'^checkout/success/$', checkout_done_view, name='success'),
    




]



