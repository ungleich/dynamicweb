from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin


@plugin_pool.register_plugin
class SectionWithImagePlugin(CMSPluginBase):
    model = CMSPlugin
    render_template = "ungleich_page/glasfaser/section_with_image.html"
    cache = False


@plugin_pool.register_plugin
class SectionContact(CMSPluginBase):
    model = CMSPlugin
    render_template = "ungleich_page/glasfaser/section_contact.html"
    cache = False
