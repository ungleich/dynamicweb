from .base import *

DEBUG = True 

ADMINS = (
    ('Nico Schottelius', 'nico.schottelius@ungleich.ch'),
    ('Raul Ascencio', 'raul.ascencio@yandex.com'),
)
#    ('Sanghee Kim', 'sanghee.kim@ungleich.ch'),

MANAGERS = ADMINS

ALLOWED_HOSTS = [
    ".ungleich.ch",
    "digital.glarus.ungleich.ch" ,
]
