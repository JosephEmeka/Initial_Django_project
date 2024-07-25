import os
from .general import *

SECRET_KEY = 'django-insecure-wb!_m@s^&$0u-j=(%^mr5th22dedn--e#4u!z^*17l4=c06c@d'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'account_db',
        'USER': 'root',
        'PASSWORD': os.environ.get('PG_ADMIN_PASSWORD'),
        'HOST': 'localhost',
    }

}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525
DEFAULT_FROM_EMAIL = 'info@jagudabank.com'
