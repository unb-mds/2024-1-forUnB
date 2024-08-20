import os
from .base import *

environment = os.getenv('DJANGO_ENVIRONMENT', 'local')

if environment == 'production':
    from .production import *
else:
    from .local import *