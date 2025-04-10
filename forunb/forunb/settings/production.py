""" Settings for production development. """
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from .base import *
import dj_database_url


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['two024-1-forunb.onrender.com','.herokuapp.com', '.forunb.com']

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': os.getenv('CLOUDINARY_URL'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

MEDIA_URL = 'https://res.cloudinary.com/dmezdx5mc/image/upload/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
