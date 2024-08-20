""" Settings for production development. """
from forunb.env import env
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', default=False)

ALLOWED_HOSTS = ['.herokuapp.com', '.forunb.com']
