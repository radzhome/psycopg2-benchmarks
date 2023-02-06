import os


DEBUG = False
INSTALLED_APPS = [
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django_extensions',
        'db_app',
    ]

TIME_ZONE = ''
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
DB_NAME = os.environ.get('DB_NAME', 'postgres')
DB_PORT = os.environ.get('DB_PORT', '')

SECRET_KEY = 'not so secret'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        },
    }
