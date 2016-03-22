from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.wizards import wizard_base
from .models import DGGalleryPlugin, DGSupportersPlugin, Supporter
from django.utils.translation import ugettext as _

class CMSGalleryPlugin(CMSPluginBase):
    model = DGGalleryPlugin
    name = _("Digital Glarus Gallery")
    render_template = "digitalglarus/gallery.html"

    def render(self, context, instance, placeholder):
        context.update({
            'gallery':instance.dgGallery,
            'object':instance,
            'placeholder':placeholder
        })
        return context

class CMSSupportersPlugin(CMSPluginBase):
    name = _("Digital Glarus Supporters")
    model = DGSupportersPlugin
    render_template = "digitalglarus/supporters_plugin.html"

    def render(self, context, instance, placeholder):
        context.update({
            'supporters': Supporter.objects.all().order_by('name'),
            'object': instance,
            'placeholder':placeholder
        })
        return context



plugin_pool.register_plugin(CMSGalleryPlugin)
plugin_pool.register_plugin(CMSSupportersPlugin)
