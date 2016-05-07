from django.db import models


class VMPlansManager(models.Manager):

    def active(self, user, **kwargs):
        return self.prefetch_related('hosting_orders__customer__user').\
            filter(hosting_orders__customer__user=user, hosting_orders__approved=True, **kwargs)\
            .distinct()
