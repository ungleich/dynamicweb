from django.contrib import admin
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from .cms_models import CMSIntegration


class CMSIntegrationAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    pass


admin.site.register(CMSIntegration, CMSIntegrationAdmin)
