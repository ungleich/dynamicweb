from django.db import models
from cms.models import CMSPlugin
from filer.fields.image import FilerImageField


class Message(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=200)
    message = models.TextField()

    received_date = models.DateTimeField('date received')

    def __str__(self):
        return "%s - %s - %s" % (self.name, self.email, self.received_date)


class Supporter(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s" % (self.name)

    def get_absolute_url(self):
        return reverse('dgSupporters_view', args=[self.pk])


class DGGallery(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return "%s" % (self.name)

    def get_absolute_url(self):
        return reverse('dgGallery_view', args=[self.pk])

    class Meta:
        verbose_name_plural = 'dgGallery'

class DGPicture(models.Model):
    gallery = models.ForeignKey(DGGallery)
    image =  FilerImageField(related_name='dg_gallery')
    description = models.CharField(max_length=60)

    def __str__(self):
        return "%s" % (self.image.name)

class DGGalleryPlugin(CMSPlugin):
    dgGallery = models.ForeignKey(DGGallery)

class DGSupportersPlugin(CMSPlugin):
    pass
