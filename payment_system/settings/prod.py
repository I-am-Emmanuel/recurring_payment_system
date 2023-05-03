import os
import dj_database_url

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', '0').lower() in ['true', 't', '1']



ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'), conn_max_age=600),
}

PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')