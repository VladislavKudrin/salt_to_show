from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView, RedirectView
from billing.views import payment_method_view, payment_method_createview
from addresses.views import *
from accounts.views import RegisterLoginView, WishListView, wishlistupdate, region_init, ProfileView
from .views import home_page, ContactPageView, AboutPageView, PrivacyPageView, TermsPageView, FAQPageView
from carts.views import cart_detail_api_view
from marketing.views import MarketingPreferenceUpdateView, MailChimpWebhookView



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('language_pref.urls')),
    url(r'^$', home_page, name = 'home'),
    url(r'^messages/', include('chat_ecommerce.urls', namespace='chat')),
    # url(r'^upload/', include('django_file_form.urls')),
    url(r'^login/$', RegisterLoginView.as_view(), name='login'),
    url(r'^social-auth/', include('social_django.urls', namespace="social")),
    url(r'^checkout/address/create/$', checkout_address_create_view, name='checkout_address_create'),
    url(r'^checkout/address/reuse/$', checkout_address_reuse_view, name='checkout_address_reuse'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^contact/$', ContactPageView.as_view(), name='contact'),
    url(r'^about/$', AboutPageView.as_view(), name='about'),
    url(r'^address/$', RedirectView.as_view(url='/addresses')),
    url(r'^addresses/$', AddressListView.as_view(), name='addresses'),
    url(r'^addresses/create/$', AddressCreateView.as_view(), name='address-create'),
    url(r'^addresses/(?P<pk>\d+)/$', AddressUpdateView.as_view(), name='address-update'),
    url(r'^search/', include("search.urls",namespace='search')),
    url(r'^bootstrap/$', TemplateView.as_view(template_name='bootstrap/example.html')),
    url(r'^products/', include("products.urls",namespace='products')), #namespace классифицирует адрес, так как у одного имени может быть несколько адресов
    url(r'^filter/', include("categories.urls",namespace='categories')),
    url(r'^settings/email/$', MarketingPreferenceUpdateView.as_view(),name='marketing-pref'),
    url(r'^settings/$', RedirectView.as_view(url='/account')),
    url(r'^webhooks/mailchimp/$', MailChimpWebhookView.as_view(),name='webhook-mailchimp'),
    url(r'^checkout/payment/', include('billing.urls', namespace='payment')),
   #url(r'^accounts/login/$', RedirectView.as_view(url='/login') ),
    url(r'^accounts/login/$', RedirectView.as_view(url='/account')),
    url(r'^accounts/$', RedirectView.as_view(url='/account')),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/account')),
    url(r'^account/', include("accounts.urls",namespace='accounts')),
    url(r'^account/', include("accounts.passwords.urls")),
    url(r'^orders/', include("orders.urls", namespace='orders')),
    url(r'^billing/payment-method/$', payment_method_view, name='billing-payment-method'),
    url(r'^billing/payment-method/create/$', payment_method_createview, name='billing-payment-method-endpoint'),
    url(r'^region-init/$', region_init, name = 'region-init'),
    url(r'^privacy/$', PrivacyPageView.as_view(), name='privacy'),
    url(r'^terms/$', TermsPageView.as_view(), name='terms'),
    url(r'^faq/$', FAQPageView.as_view(), name='faq'),
    url(r'^users/(?P<username>[\w.@+-]+)/$', ProfileView.as_view(), name='profile'), 
    url(r'^api/', include('bot.urls', namespace="api")),

]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#        url(r'^__debug__/', include(debug_toolbar.urls)),] + urlpatterns




if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns


admin.site.site_header = 'SALT ADMIN'                    # default: "Django Administration"
admin.site.index_title = 'SALT ADMIN'                   # default: "Site administration"
admin.site.site_title = 'SALT'                          # default: "Django site admin"


