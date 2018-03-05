from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin

from .cms_models import (
    DCLBannerItemPluginModel, DCLBannerListPluginModel, DCLContactPluginModel,
    DCLFooterPluginModel, DCLLinkPluginModel, DCLNavbarDropdownPluginModel,
    DCLSectionIconPluginModel, DCLSectionImagePluginModel,
    DCLSectionPluginModel,
)
from .models import VMTemplate


@plugin_pool.register_plugin
class DCLSectionPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Section Plugin"
    model = DCLSectionPluginModel
    render_template = "datacenterlight/cms/section.html"
    cache = False
    allow_children = True
    child_classes = ['DCLSectionIconPlugin', 'DCLSectionImagePlugin']


@plugin_pool.register_plugin
class DCLSectionIconPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Section Icon Plugin"
    model = DCLSectionIconPluginModel
    render_template = "datacenterlight/cms/section_icon.html"
    cache = False
    require_parent = True


@plugin_pool.register_plugin
class DCLSectionImagePlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Section Image Plugin"
    model = DCLSectionImagePluginModel
    render_template = "datacenterlight/cms/section_image.html"
    cache = False
    require_parent = True


@plugin_pool.register_plugin
class DCLCalculatorPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Calculator Plugin"
    model = DCLSectionPluginModel
    render_template = "datacenterlight/cms/calculator.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super(DCLCalculatorPlugin, self).render(
            context, instance, placeholder
        )
        context['templates'] = VMTemplate.objects.all()
        return context


@plugin_pool.register_plugin
class DCLBannerListPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Banner List Plugin"
    model = DCLBannerListPluginModel
    render_template = "datacenterlight/cms/banner_list.html"
    cache = False
    allow_children = True
    child_classes = ['DCLBannerItemPlugin']


@plugin_pool.register_plugin
class DCLBannerItemPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Banner Item Plugin"
    model = DCLBannerItemPluginModel
    render_template = "datacenterlight/cms/banner_item.html"
    cache = False
    require_parent = True
    parent_classes = ['DCLBannerListPlugin']


@plugin_pool.register_plugin
class DCLNavbarPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Navbar Plugin"
    model = CMSPlugin
    render_template = "datacenterlight/cms/navbar.html"
    cache = False
    allow_children = True
    child_classes = ['DCLLinkPlugin', 'DCLNavbarDropdownPlugin']


@plugin_pool.register_plugin
class DCLNavbarDropdownPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Navbar Dropdown Plugin"
    model = DCLNavbarDropdownPluginModel
    render_template = "datacenterlight/cms/navbar_dropdown.html"
    cache = False
    allow_children = True
    child_classes = ['DCLLinkPlugin']
    require_parent = True
    parent_classes = ['DCLNavbarPlugin']


@plugin_pool.register_plugin
class DCLLinkPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Link Plugin"
    model = DCLLinkPluginModel
    render_template = "datacenterlight/cms/link.html"
    cache = False
    require_parent = True


@plugin_pool.register_plugin
class DCLContactPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Contact Plugin"
    model = DCLContactPluginModel
    render_template = "datacenterlight/cms/contact.html"
    cache = False


@plugin_pool.register_plugin
class DCLFooterPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Footer Plugin"
    model = DCLFooterPluginModel
    render_template = "datacenterlight/cms/footer.html"
    cache = False
    allow_children = True
    child_classes = ['DCLLinkPlugin']
