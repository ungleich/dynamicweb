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
    title = models.CharField(max_length=400)


class SectionWithImage(UngelichPicture):
    price_tag_image = FilerImageField(
        null=True,
        blank=True,
        related_name="price_tag_image",
        on_delete=models.SET_NULL
    )
    price_tag_url = models.URLField(max_length=300, default="")


class UngelichContactUsSection(CMSPlugin):
    email = models.EmailField(max_length=200)


class UngelichTextSection(CMSPlugin):
    title = models.CharField(max_length=200)
    description = HTMLField()


class Service(CMSPlugin):
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class ServiceItem(CMSPlugin):
    image = FilerImageField(
        null=True,
        blank=True,
        related_name="service_item_image",
        on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=200)
    description = HTMLField()

    def __str__(self):
        return self.title


class About(Service):
    pass


class AboutItem(UngelichPicture):
    inverted = models.BooleanField(default=False)

    def __str__(self):
        alignment = "Right" if self.inverted else "Left"
        return "{alignment} - {title}".format(
            alignment=alignment, title=self.title
        )
