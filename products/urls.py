from django.conf.urls import url



from .views import (
    ProductListView, 
    ProductDetailSlugView,
    ProductCreateView,
    AccountProductListView,
    ProductUpdateView,
    product_delete,
    ProductDeleteView,
<<<<<<< HEAD
    # WishListView,
    # wishlistupdate,
=======
    WishListView,
    wishlistupdate,
    handle_upload,
    image_update_view
>>>>>>> vlad

    )


urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='list'),
    url(r'^handle_image_sort$', image_update_view, name='handle_image_sort'),
    url(r'^create/$', ProductCreateView.as_view(), name='create'),
    url(r'^list/$', AccountProductListView.as_view(), name='user-list'),
    # url(r'^wish-list/$', WishListView.as_view(), name='wish-list'),
    # url(r'^wishlist-update/$', wishlistupdate, name='wish-list-update'),
    url(r'^delete/$', product_delete, name='delete'),
<<<<<<< HEAD
    url(r'^update/(?P<slug>[\w-]+)/$', ProductUpdateView.as_view(), name='update'),
    url(r'^update/(?P<slug>[\w-]+)/$', ProductDeleteView.as_view(), name='delete'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
=======
    url(r'^update/(?P<slug>[\w.@+-]+)/$', ProductUpdateView.as_view(), name='update'),
    url(r'^delete/(?P<slug>[\w.@+-]+)/$', ProductDeleteView.as_view(), name='delete'),
    url(r'^view/(?P<slug>[\w.@+-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
    url(r'^handle_upload$', handle_upload, name='example_handle_upload'),
    url(r'^existing/(?P<id>\d+)$', ProductUpdateView.as_view(), name='existing_file_example'),

>>>>>>> vlad


]



