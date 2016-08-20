from django.db import models
from cms.models import CMSPlugin
from filer.fields.image import FilerImageField
from django.core.urlresolvers import reverse


class MembershipType(models.Model):

    MEMBERSHIP_TYPES = (
        ('standard', 'Standard'),

    )
    name = models.CharField(choices=MEMBERSHIP_TYPES, max_length=20)
    price = models.FloatField()


class Membership(models.Model):
    type = models.ForeignKey(MembershipType)

    @classmethod
    def create(cls, data, user):
        instance = cls.objects.create(**data)
        instance.assign_permissions(user)
        return instance


class MembershipOrder(models.Model):
    membership = models.ForeignKey(Membership)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    last4 = models.CharField(max_length=4)
    cc_brand = models.CharField(max_length=10)
    stripe_charge_id = models.CharField(max_length=100, null=True)


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
#
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
