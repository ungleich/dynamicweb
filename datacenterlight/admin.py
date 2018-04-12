from django.contrib import admin
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from cms.extensions import PageExtensionAdmin
from .cms_models import CMSIntegration, CMSFaviconExtension


class CMSIntegrationAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'domain')


class CMSFaviconExtensionAdmin(PageExtensionAdmin):
    pass


admin.site.register(CMSIntegration, CMSIntegrationAdmin)
admin.site.register(CMSFaviconExtension, CMSFaviconExtensionAdmin)
