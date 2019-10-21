import datetime
# from storages.backends.s3boto3 import S3Boto3Storage


AWS_GROUP_NAME = 'EnvisionGroup'
AWS_USERNAME = 'envision-user'
AWS_ACCESS_KEY_ID = 'AKIA2R5PIZK6CADVS36G'
AWS_SECRET_ACCESS_KEY = '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'
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True





DEFAULT_FILE_STORAGE = 'ecommerce.aws.utils.MediaRootS3BotoStorage'
FILE_FORM_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'ecommerce.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'salt-bucket-eu'
AWS_BUCKET_NAME = 'salt-bucket-eu'
S3DIRECT_REGION = 'eu-central-1'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
FILE_FORM_UPLOAD_DIR = '//%s.s3.amazonaws.com/media/temp_uploads/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

AWS_UPLOAD_CLIENT_KEY = AWS_ACCESS_KEY_ID
AWS_UPLOAD_CLIENT_SECRET_KEY = AWS_SECRET_ACCESS_KEY

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = { 
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}

AWS_QUERYSTRING_AUTH = False