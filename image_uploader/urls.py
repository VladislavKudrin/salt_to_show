from django.conf.urls import url

from .views import (
	handle_upload,
	handle_delete,
	handle_rotate
	)


urlpatterns = (
    url(r'^handle_upload$', handle_upload, name='image_upload_url'),
    url(r'^handle_delete$', handle_delete, name='image_delete_url'),
    url(r'^handle_rotate$', handle_rotate, name='image_rotate_url'),
)
