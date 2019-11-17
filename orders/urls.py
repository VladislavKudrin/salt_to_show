from django.conf.urls import url


from .views import (
	OrderListView,
	OrderDetailView,
	transaction_initiation_view
    )

 

urlpatterns = [
    url(r'^$',OrderListView.as_view(), name='list'),
    url(r'^transaction_initiate/$',transaction_initiation_view, name='transaction_initiate'),
    url(r'^(?P<order_id>[0-9A-Za-z]+)/$',OrderDetailView.as_view(), name='detail'),


]



