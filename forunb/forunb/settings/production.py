""" Settings for production development. """
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from .base import *
import dj_database_url
from decouple import config


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com', '.forunb.com']

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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'  # Isso é literal, use 'apikey' como o usuário
EMAIL_HOST_PASSWORD = config('SENDGRID_API_KEY')  # A chave de API gerada no Heroku
DEFAULT_FROM_EMAIL = 'noreply@forunb.com'