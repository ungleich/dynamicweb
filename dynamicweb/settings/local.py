from .base import * # flake8: noqa

REGISTRATION_MESSAGE['message'] = REGISTRATION_MESSAGE['message'].format(host='dynamicweb-development.ungleich.ch',
                                                                         slug='{slug}')
ALLOWED_HOSTS = [
    "*"
    ]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

MIDDLEWARE_CLASSES += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

INSTALLED_APPS += (
    'django_extensions',
    'debug_toolbar'
    )
