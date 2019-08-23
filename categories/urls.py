from django.conf.urls import url



from .views import (
        CategoryFilterView,
        translation_view,


    )


#adelia test
urlpatterns = [
    url(r'^$', CategoryFilterView.as_view(), name='filter'),
    url(r'^translate/$', translation_view, name='translate')
]

