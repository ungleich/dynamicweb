from django.db import models


class VMPlansManager(models.Manager):

    def active(self, user, **kwargs):
        return self.select_related('hostingorder__customer__user').\
            filter(hostingorder__customer__user=user, hostingorder__approved=True, **kwargs)
