import os
import urlparse

import dj_database_url

from .settings import *

# Parse database configuration from $DATABASE_URL
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

INSTALLED_APPS += (
    'storages',
)

# Static asset configuration
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '..', 'static'),
)

# make debug easier to flip on and off
DEBUG = os.environ.get('DEBUG', False) == 'True'

# MEDIA files serving
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', None)

# We are explicitly _not_ setting this because we are using Kenneth Reitz's
# dj_static app to serve static media from Heroku. Because hey ... free
# bandwidth at Heroku!
# STATICFILES_STORAGE = '(remove_me)storages.backends.s3boto.S3BotoStorage'

# see http://developer.yahoo.com/performance/rules.html#expires
AWS_HEADERS = {
    'Expires': 'Tue, 21 Jun 2016 20:00:00 GMT', # something about that date ...
}
