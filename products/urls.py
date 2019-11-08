from django.conf.urls import url
from .views import *
from categories.views import CategoryFilterView


urlpatterns = [
    url(r'^$', CategoryFilterView.as_view(), name='list'),
    url(r'^handle_image_sort$', image_update_view, name='handle_image_sort'),
    url(r'^handle_image_create_sort$', image_create_order, name='handle_image_create_sort'),
    url(r'^create/$', ProductCreateView.as_view(), name='create'),
    url(r'^list/$', AccountProductListView.as_view(), name='user-list'),
    url(r'^delete/$', product_delete, name='delete'),
    url(r'^report/$', product_report, name='report'),
    url(r'^update/(?P<slug>[\w.@+-]+)/$', ProductUpdateView.as_view(), name='update'),
    url(r'^delete/(?P<slug>[\w.@+-]+)/$', ProductDeleteView.as_view(), name='delete'),
    url(r'^view/(?P<slug>[\w.@+-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
    url(r'^existing/(?P<id>\d+)$', ProductUpdateView.as_view(), name='existing_file_example'),
    url(r'^report/$', product_report, name='report'),
    url(r'^fakelist/$', FakeProductsListView.as_view(), name='fake-list'),
    url(r'^(?P<filter>[\w.@+-=&]+)$', CategoryFilterView.as_view(), name='list-filter'),
]



