
from django.conf.urls import url

from . import views


urlpatterns = (
	url(r'^$', views.rendertest, name='test'),
    url(r'^hi$', views.ExampleView.as_view(), name='example'),
    url(r'^success$', views.ExampleSuccessView.as_view(), name='example_success'),
    url(r'^multiple$', views.MultipleExampleView.as_view(), name='multiple_example'),
    url(r'^multiple_without_js$', views.MultipleWithoutJsExampleView.as_view(), name='multiple_without_js_example'),
    url(r'^existing/(?P<id>\d+)$', views.ExistingFileExampleView.as_view(), name='existing_file_example'),
    url(r'^handle_upload$', views.handle_upload, name='example_handle_upload'),


)
















# from django.conf.urls import url


# from .views import (
# 	TestCreateView
#     )



# urlpatterns = [
#     url(r'^$',TestCreateView.as_view(), name='test'),



# ]



