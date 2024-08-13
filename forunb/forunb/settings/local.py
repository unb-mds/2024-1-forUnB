""" Settings for local development. """
from forunb.env import env
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', default=True)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=['localhost', '0.0.0.0', '127.0.0.1'])
