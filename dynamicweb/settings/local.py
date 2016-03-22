from .base import *

ALLOWED_HOSTS = [
    "*"
    ]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'app.db',
#     }
# }
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}
MIDDLEWARE_CLASSES+=("debug_toolbar.middleware.DebugToolbarMiddleware",)


DEBUG = True
