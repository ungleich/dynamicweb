from django.contrib import admin
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from .cms_models import CMSIntegration
from .models import VMPricing


class CMSIntegrationAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'domain')


admin.site.register(CMSIntegration, CMSIntegrationAdmin)
admin.site.register(VMPricing)
