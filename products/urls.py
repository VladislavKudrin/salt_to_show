from django.conf.urls import url



from .views import (
    ProductListView, 
    ProductDetailSlugView,
    ProductCreateView,
    AccountProductListView,
    ProductUpdateView,
    ProductDeleteView,
    product_delete


    )


#adelia test
urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='list'),
    url(r'^create/$', ProductCreateView.as_view(), name='create'),
    url(r'^list/$', AccountProductListView.as_view(), name='user-list'),
    url(r'^delete/$', product_delete, name='delete'),
    url(r'^update/(?P<slug>[\w-]+)/$', ProductUpdateView.as_view(), name='update'),
    url(r'^delete/(?P<slug>[\w-]+)/$', ProductDeleteView.as_view(), name='delete'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),

]



