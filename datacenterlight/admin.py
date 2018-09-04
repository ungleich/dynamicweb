from django.contrib import admin
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from cms.extensions import PageExtensionAdmin
from .cms_models import CMSIntegration, CMSFaviconExtension
from .models import VMPricing, VMTemplate


class CMSIntegrationAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'domain')


class CMSFaviconExtensionAdmin(PageExtensionAdmin):
    pass


admin.site.register(CMSIntegration, CMSIntegrationAdmin)
admin.site.register(CMSFaviconExtension, CMSFaviconExtensionAdmin)
admin.site.register(VMPricing)
admin.site.register(VMTemplate)
