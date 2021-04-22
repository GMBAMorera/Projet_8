from . import *
import os

SECRET_KEY = os.getenv('SECRET_KEY_PROD')

DEBUG = False

ALLOWED_HOSTS = ['142.93.232.237']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ocpurbeurre',
        'USER': 'georges',
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432'
        }
}

