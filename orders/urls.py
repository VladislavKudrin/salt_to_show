from django.conf.urls import url


from .views import (
	OrderListView,
	OrderDetailView,
	order_complete_view

    )

 

urlpatterns = [
    url(r'^$',OrderListView.as_view(), name='list'),
    url(r'^complete_order/$',order_complete_view, name='complete_order'),
    url(r'^(?P<order_id>[0-9A-Za-z]+)/$',OrderDetailView.as_view(), name='detail'),



]



