from cms.models.pluginmodel import CMSPlugin
from django.db import models
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField


class UngelichPicture(CMSPlugin):
    image = FilerImageField(
        null=True,
        blank=True,
        related_name="image",
        on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=200)


class UngelichContactUsSection(CMSPlugin):
    email = models.EmailField(max_length=200)


class UngelichTextSection(CMSPlugin):
    title = models.CharField(max_length=200)
    description = HTMLField()
