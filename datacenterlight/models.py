from django.db import models

# Create your models here.


class BetaAccess(models.Model):
    email = models.CharField(max_length=250)

    def __str__(self):
        return self.email
