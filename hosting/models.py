from django.db import models

class RailsBetaUser(models.Model):
    email = models.EmailField(unique=True)
    received_date = models.DateTimeField('date received')

    def __str__(self):
        return "%s - %s" % (self.email, self.received_date)
