""" Settings for production development. """
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com', '.forunb.com', 'forunb-201a551c5a00.herokuapp.com']
