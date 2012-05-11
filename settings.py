DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('NAME SURNAME', 'email@address.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'DB NAME',
        'USER': 'DB USER',
        'PASSWORD': 'DB PASS',
        'HOST': '', # localhost by default 
        'PORT': '', # 3306 by defalult
    }
}

SECRET_KEY = 'YOUR SECRET KEY'

# Stripe test keys (do not forget to switch them for the production keys later)
STRIPE_PUBLIC_KEY = 'YOUR STRIPE PUBLIC KEY'
STRIPE_PRIVATE_KEY = 'YOUR STRIPE PRIVATE KEY'

from common_settings import *