from .base import *

# List of people that get admin messages
ADMINS = ( (x, x + "@ungleich.ch") for x in ["web-team"] )

DEBUG=False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#MANAGERS = ADMINS

REGISTRATION_MESSAGE['message'] = REGISTRATION_MESSAGE['message'].format(host='digitalglarus.ungleich.ch',slug='{slug}')

ALLOWED_HOSTS = [
    ".ungleich.ch",
    "digital.glarus.ungleich.ch",
    ".alplora.ch"
]
