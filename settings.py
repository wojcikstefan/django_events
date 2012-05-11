DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Stefan Wojcik', 'wojcikstefan@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_events',
        'USER': 'django_events',
        'PASSWORD': 'secret_pass',
        'HOST': '',
        'PORT': '',
    }
}

# Stripe test keys
STRIPE_PUBLIC_KEY = 'pk_klRyAO6DqsgBoboM8qOyeH1mPzl3U'
STRIPE_PRIVATE_KEY = 'QUI20VjqU5h8mNcfUP0nQVUAs80nFAUZ'

from common_settings import *