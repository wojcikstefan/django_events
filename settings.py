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

from common_settings import *