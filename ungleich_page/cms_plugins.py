from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import (
    UngelichPicture, UngelichContactUsSection, UngelichTextSection
)


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
    model = UngelichContactUsSection
    render_template = "ungleich_page/glasfaser/section_contact.html"
    cache = False


@plugin_pool.register_plugin
class SectionTextParagraphDCL(CMSPluginBase):
    model = UngelichTextSection
    render_template = "ungleich_page/glasfaser/section_text_dcl.html"
    cache = False


@plugin_pool.register_plugin
class SectionTextParagraphGlasfaser(CMSPluginBase):
    model = UngelichTextSection
    render_template = "ungleich_page/glasfaser/section_text_glasfaser.html"
    cache = False
