from django.contrib import admin
from cms.extensions import PageExtensionAdmin

# Register your models here.

from .models import UngleichPage


class UngleichPageAdmin(PageExtensionAdmin):
    pass


admin.site.register(UngleichPage, UngleichPageAdmin)
