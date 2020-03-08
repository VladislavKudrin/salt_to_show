from django.conf.urls import url


from .views import (
	OrderListView,
	OrderDetailView,
	order_complete_view,
	order_track_view,
	order_delete_view,
    order_give_feedback

    )

 

urlpatterns = [
    url(r'^$',OrderListView.as_view(), name='list'),
    url(r'^complete_order/$',order_complete_view, name='complete_order'),
    url(r'^track_order/$',order_track_view, name='track_order'),
    url(r'^delete_order/$',order_delete_view, name='delete_order'),
    url(r'^give_feedback/$',order_give_feedback, name='feedback'),
    # url(r'^(?P<order_id>[0-9A-Za-z]+)/$',OrderDetailView.as_view(), name='detail'),



]



