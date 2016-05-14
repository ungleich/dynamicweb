from django.db import models

from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool
from filer.fields.image import FilerImageField


# Create your models here.


class UngleichPage(PageExtension):
    #image_header = models.ImageField(upload_to='image_header')
    image = FilerImageField(null=True, blank=True,
                           related_name="ungleinch_page_image")

    class Meta:
        app_label = 'ungleich'

extension_pool.register(UngleichPage)
