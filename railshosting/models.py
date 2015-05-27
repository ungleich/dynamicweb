from django.db import models

class RailsBetaUSer(models.Model):
    email = models.EmailField(unique=True)
    received_date = models.DateTimeField('date received')

    def __str__(self):
        return "%s - %s" % (self.email, self.received_date)
