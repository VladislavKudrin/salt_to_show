"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 1.11.18.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
MAX_UPLOAD_SIZE = "20971520"
CONTENT_TYPES = ['image', 'video']

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
    
ALLOWED_HOSTS = ['.saltish.co', 'salt-eu.herokuapp.com']

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'info@saltish.co' 
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'SALT <info@saltish.co>'
BASE_URL = 'https://www.saltish.co'

MANAGERS = (
    ('Vladislav Kudrin', "info@saltish.co" ),
)

ADMINS = MANAGERS

WSGI_APPLICATION = 'ecommerce.wsgi.application'
ASGI_APPLICATION = 'ecommerce.routing.application'

SESSION_EXPIRE_AT_BROWSER_CLOSE = False


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    #third party
    'storages',
    'social_django',
    'crispy_forms',
    'sass_processor',
    'rest_framework',
    'dj_pagination',

    #our apps
    'chat_ecommerce',
    'addresses',
    'products',
    'search',
    'tags',
    'analitics',
    'carts',
    'marketing',
    'orders',
    'accounts',
    'billing',
    'categories',
    'image_uploader'
]

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/login/'
LOGIN_URL_REDIRECT = '/'
LOGOUT_URL = '/logout/'
#SESSION OPTIONS
FORCE_SESSION_TO_ONE = False
FORCE_INACTIVE_USER_ENDSESSION = True

# import stripe
# STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
# STRIPE_PUB_KEY =  os.environ.get('STRIPE_PUB_KEY')
# stripe.api_key = STRIPE_SECRET_KEY

#CRISPY 
CRISPY_TEMPLATE_PACK = 'bootstrap4'

#MAILCHIMP
MAILCHIMP_API_KEY           = os.environ.get('MAILCHIMP_API_KEY')
MAILCHIMP_DATA_CENTER       = 'us20'
MAILCHIMP_EMAIL_LIST_ID     = os.environ.get('MAILCHIMP_EMAIL_LIST_ID')

#SOCIAL_AUTH
SOCIAL_AUTH_VK_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_VK_OAUTH2_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_VK_OAUTH2_SECRET')
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']

#GOOGLE 
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '940431062117-rs5fjkdr1kv6u8knopnoh0v6bp7bs29r.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '0DxTUlxTO2zgi3-D1Lgl18q2'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']
#PRIVATE_CHAT
CHAT_WS_SERVER_HOST = 'localhost'
CHAT_WS_SERVER_PORT = 5002
CHAT_WS_SERVER_PROTOCOL = 'ws'

#SASS
SASS_PROCESSOR_INCLUDE_DIRS = (
    os.path.join(BASE_DIR, 'static_my_project/bootstrap-4.1.3'),
    os.path.join(BASE_DIR, 'static_my_project/custom_scss'),
)

SASS_PROCESSOR_INCLUDE_FILE_PATTERN = r'^.+\.scss$'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
)

AUTHENTICATION_BACKENDS = [
        'social_core.backends.vk.VKOAuth2',
        'django.contrib.auth.backends.ModelBackend',
        'social_core.backends.google.GooglePlusAuth',
        'social_core.backends.open_id.OpenIdAuth',
        'social_core.backends.google.GoogleOAuth2',
        ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #third party
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'dj_pagination.middleware.PaginationMiddleware',
]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',
    'accounts.views.add_message',
    # 'social_core.pipeline.user.make_active',

)




LOGOUT_REDIRECT_URL='/login/'
ROOT_URLCONF = 'ecommerce.urls'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  # <- Here
                'social_django.context_processors.login_redirect', # <- Here
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request"
            ],
        },
    },
]

PAGINATION_DEFAULT_WINDOW = 2
PAGINATION_DEFAULT_MARGIN = 1
PAGINATION_DEFAULT_PAGINATION = 20 #number per page
PAGINATION_DISPLAY_PAGE_LINKS = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
#Heroku database
import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)



# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
DEFAULT_LANGUAGE_PREF = 'EN'



TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/



CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')], # for heroku in keys vars
        },
    #"symmetric_encryption_keys": [SECRET_KEY],
    },
}

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static_my_project"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "live-static-files", "static-root")



STATIC_URL = '/static/'

# MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "live-static-files", "media-root")

from ecommerce.aws.conf import *

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240
DATA_UPLOAD_MAX_MEMORY_SIZE = 500000000 # value in bytes
IMAGES_UPLOAD_LIMIT = 8
IMAGES_UPLOAD_MIN = 4
IMAGES_QUALITY_THUMBNAIL_PRECENTAGE = 100
IMAGES_THUMBNAIL_SIZE = (600, 600)

# CACHES = {
#     "default": {
#          "BACKEND": "redis_cache.RedisCache",
#          "LOCATION": os.environ.get('REDIS_URL'),
#     }
# }


#Let's Encrypt ssl/tls https

CORS_REPLACE_HTTPS_REFERER      = True
HOST_SCHEME                     = "https://"
SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT             = True
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_SECONDS             = 1000000
SECURE_FRAME_DENY               = True


PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 10,
    'MARGIN_PAGES_DISPLAYED': 2,

    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}




