from .base import *

ADMINS = (
    ('Nico Schottelius', 'nico.schottelius@ungleich.ch'),
    ('Raul Ascencio', 'raul.ascencio@yandex.com'),
    ('Web team', 'web-team@ungleich.ch')

)
#    ('Sanghee Kim', 'sanghee.kim@ungleich.ch'),
DEBUG=False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#MANAGERS = ADMINS

REGISTRATION_MESSAGE['message'] = REGISTRATION_MESSAGE['message'].format(host='digitalglarus.ungleich.ch',slug='{slug}')

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
