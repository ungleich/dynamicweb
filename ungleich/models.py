from django.db import models

from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool


# Create your models here.

class UngleichPage(PageExtension):
    image_header = models.ImageField(upload_to='image_header')

extension_pool.register(UngleichPage)
