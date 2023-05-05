from . common import *
import environ

DEBUG = True



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"),
        'PORT': env('DB_PORT'),

    }
}

SECRET_KEY = env('SECRET_KEY')

# this call the paystack secret key I already set in my .env file
PAYSTACK_SECRET_KEY = env('PAYSTACK_SECRET_KEY')



