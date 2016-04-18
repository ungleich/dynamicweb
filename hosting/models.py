from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import serializers




class RailsBetaUser(models.Model):
    email = models.EmailField(unique=True)
    received_date = models.DateTimeField('date received')

    def __str__(self):
        return "%s - %s" % (self.email, self.received_date)


class VirtualMachineType(models.Model):

    HETZNER_NUG = 'hetzner_nug'
    HETZNER = 'hetzner'
    HETZNER_R6 = 'hetzner_raid6'
    HETZNER_G = 'hetzner_glusterfs'
    BERN = 'bern'

    HOSTING_TYPES = (
        (HETZNER_NUG, 'Hetzner No Uptime Guarantee'),
        (HETZNER, 'Hetzner'),
        (HETZNER_R6, 'Hetzner Raid6'),
        (HETZNER_G, 'Hetzner Glusterfs'),
        (BERN, 'Bern'),
    )

    description = models.TextField()
    base_price = models.FloatField()
    memory_price = models.FloatField()
    core_price = models.FloatField()
    disk_size_price = models.FloatField()
    hosting_company = models.CharField(max_length=10, choices=HOSTING_TYPES)

    def get_serialized_data(self):
        return serializers("json", self)
