import datetime
from django.conf import settings


AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True



DEFAULT_FILE_STORAGE = 'ecommerce.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'ecommerce.aws.utils.StaticRootS3BotoStorage'
if settings.TESTSERVER == 'True':
	AWS_STORAGE_BUCKET_NAME = 'salt-staging'
	AWS_ACCESS_KEY_ID = "AKIA2R5PIZK6FDQ5PRUR"
	AWS_SECRET_ACCESS_KEY = "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"
	AWS_GROUP_NAME = 'Salt-Staging'
	AWS_USERNAME = 'salt-staging'
else:
	AWS_STORAGE_BUCKET_NAME = 'salt-bucket-eu'
	AWS_ACCESS_KEY_ID = "AKIA2R5PIZK6M3HVE26S"
	AWS_SECRET_ACCESS_KEY = "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"
	AWS_GROUP_NAME = 'EnvisionGroup'
	AWS_USERNAME = 'envision-user'

S3DIRECT_REGION = 'eu-central-1'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=1)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_S3_OBJECT_PARAMETERS = { 
    'Expires': expires,
    'CacheControl': 'max-age=%d' % (int(two_months.total_seconds()), ),
}
AWS_QUERYSTRING_AUTH = False
AWS_IS_GZIPPED = True




