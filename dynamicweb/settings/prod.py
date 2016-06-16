from .base import *

ADMINS = (
    ('Nico Schottelius', 'nico.schottelius@ungleich.ch'),
    ('Raul Ascencio', 'raul.ascencio@yandex.com'),
    ('Tomislav Rupcic','tmslav@gmail.com'),

)
#    ('Sanghee Kim', 'sanghee.kim@ungleich.ch'),

EMAIL_BACKEND = "mailer.backend.DbBackend"

#MANAGERS = ADMINS

REGISTRATION_MESSAGE['message'] = REGISTRATION_MESSAGE['message'].format(host='digitalglarus.ungleich.ch',slug='{slug}')

ALLOWED_HOSTS = [
    ".ungleich.ch",
    "digital.glarus.ungleich.ch" ,
]
