from django.conf.urls import url
from django.contrib.auth import views as auth_views
from accounts.views import (
        PasswordResetView, 
        PasswordResetDoneView, 
        PasswordChangeView, 
        PasswordChangeDoneView,
        PasswordResetConfirmView,
        PasswordResetCompleteView
        )

urlpatterns  = [
        url(r'^password/change/$', 
                PasswordChangeView.as_view(), 
                name='password_change'),
        url(r'^password/change/done/$',
                PasswordChangeDoneView.as_view(), 
                name='password_change_done'),
        url(r'^password/reset/$', 
                PasswordResetView.as_view(), 
                name='password_reset'),
        url(r'^password/reset/done/$', 
                PasswordResetDoneView.as_view(), 
                name='password_reset_done'),
        url(r'^password/reset/\
                (?P<uidb64>[0-9A-Za-z_\-]+)/\
                (?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
                PasswordResetConfirmView.as_view(), 
                name='password_reset_confirm'),
        url(r'^password/reset/complete/$', 
                PasswordResetCompleteView.as_view(), 
                name='password_reset_complete'),
        ]

