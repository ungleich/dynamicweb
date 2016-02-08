from django.db import models


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
    description = models.TextField()
