from .base import *


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('MARIADB_DATABASE_DEV'),
        'USER': config('MARIADB_USER'),
        'PASSWORD': config('MARIADB_ROOT_PASSWORD'),
        'HOST': config('MARIADB_HOST'),
        'PORT': config('MARIADB_PORT'),
        'OPTIONS': {
            'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'
        }
    }
}