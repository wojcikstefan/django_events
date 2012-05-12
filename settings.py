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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'EMAIL HOST'
EMAIL_HOST_USER = 'EMAIL USERNAME'
EMAIL_HOST_PASSWORD = 'EMAIL PASSWORD'
EMAIL_PORT = 'EMAIL PORT (INTEGER)'
EMAIL_USE_TLS = 'USE TLS? (TRUE/FALSE)'

# Stripe test keys (do not forget to switch them for the production keys later)
STRIPE_PUBLIC_KEY = 'YOUR STRIPE PUBLIC KEY'
STRIPE_PRIVATE_KEY = 'YOUR STRIPE PRIVATE KEY'

from common_settings import *