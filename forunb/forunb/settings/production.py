""" Settings for production development. """
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com', '.forunb.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'forunb_db',
        'USER': 'forunb',
        'PASSWORD': 'balao123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
