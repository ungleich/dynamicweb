from .base import *

ADMINS = (
    ('Nico Schottelius', 'nico.schottelius@ungleich.ch'),
    ('Tomislav Rupcic','tmslav@gmail.com'),

)
#    ('Sanghee Kim', 'sanghee.kim@ungleich.ch'),
DEBUG=False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#MANAGERS = ADMINS

REGISTRATION_MESSAGE['message'] = REGISTRATION_MESSAGE['message'].format(host='digitalglarus.ungleich.ch',slug='{slug}')

ALLOWED_HOSTS = [
    ".ungleich.ch",
    "digital.glarus.ungleich.ch",
    ".alplora.ch"
]
