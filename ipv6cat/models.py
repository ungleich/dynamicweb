from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse


# Create your models here.
class Cat(models.Model):
    title = models.CharField(max_length=200)
    image = models.FileField()
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super(Cat, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ipv6cat:detail', args=[self.slug])
        