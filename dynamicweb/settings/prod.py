from .base import *  # flake8: noqa

# List of people that get admin messages
ADMINS = ((x, x + "@ungleich.ch") for x in ["web-team"])

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# MANAGERS = ADMINS

REGISTRATION_MESSAGE['message'] = REGISTRATION_MESSAGE['message'].format(host='digitalglarus.ungleich.ch',
                                                                         slug='{slug}')  # flake8: noqa

ALLOWED_HOSTS = [
    ".ungleich.ch",
    ".datacenterlight.ch",
    ".rails-hosting.ch",
    ".django-hosting.ch",
    ".node-hosting.ch",
    ".devuanhosting.ch",
    ".digitalezukunft.ch",
    ".ipv6onlyhosting.ch",
    ".ipv6onlyhosting.com",
    ".ipv6onlyhosting.net",
    ".digitalglarus.ch",
    ".alplora.ch"
]
