import os
import urlparse

from .settings import *

@property
def DATABASES():
    """Setup DATABASES setting, but hide intermediate bits"""
    url = urlparse.urlparse(os.environ['DATABASE_URL'])

    db = {
        'NAME': url.path[1:],
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port,
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
    }

    return { 'default': db }

@property
def DEBUG():
    """Set DEBUG based on env vars"""
    debug = os.environment.get('DEBUG', False)
    return debug == 'True'
