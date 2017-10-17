from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import UngelichPicture


@plugin_pool.register_plugin
class SectionWithImagePlugin(CMSPluginBase):
    model = UngelichPicture
    render_template = "ungleich_page/glasfaser/section_with_image.html"
    cache = False

    def render(self, context, instance, placeholder):
        context.update({
            'image': instance.image,
            'object': instance,
            'placeholder': placeholder
        })
        return context


@plugin_pool.register_plugin
class SectionContact(CMSPluginBase):
    model = CMSPlugin
    render_template = "ungleich_page/glasfaser/section_contact.html"
    cache = False
