from django.conf.urls import url



from .views import (
        CategoryFilterView


    )


#adelia test
urlpatterns = [
    url(r'^$', CategoryFilterView.as_view(), name='filter'),
]

