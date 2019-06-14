from django.conf.urls import url

from .views import (
	handle_upload
	)


urlpatterns = (
    url(r'^handle_upload$', handle_upload, name='image_upload_url'),
)
