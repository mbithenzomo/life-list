"""
Development specific settings for lifelist project.
"""

from .base import *

SECRET_KEY = 'AFD8F8BAE9DB456FBE26262B287DB'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_lifelist',
        'USER': 'test_user',
        'PASSWORD': 'test_password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
