from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin

from .cms_models import (
    DCLSectionPluginModel, DCLLinkPluginModel,
    DCLNavbarDropdownPluginModel, DCLContactPluginModel,
    DCLFooterPluginModel, DCLSectionIconPluginModel,
    DCLSectionImagePluginModel
)


@plugin_pool.register_plugin
class DCLCalculatorPlugin(CMSPluginBase):
    module = "Datacenterlight"
    model = DCLSectionPluginModel
    render_template = "datacenterlight/cms/calculator.html"
    cache = False


@plugin_pool.register_plugin
class DCLSectionPlugin(CMSPluginBase):
    module = "Datacenterlight"
    model = DCLSectionPluginModel
    render_template = "datacenterlight/cms/section.html"
    cache = False
    allow_children = True
    child_classes = ['DCLSectionIconPlugin', 'DCLSectionImagePlugin']


@plugin_pool.register_plugin
class DCLNavbarPlugin(CMSPluginBase):
    module = "Datacenterlight"
    model = CMSPlugin
    render_template = "datacenterlight/cms/navbar.html"
    cache = False
    allow_children = True
    child_classes = ['DCLLinkPlugin', 'DCLNavbarDropdownPlugin']


@plugin_pool.register_plugin
class DCLLinkPlugin(CMSPluginBase):
    module = "Datacenterlight"
    model = DCLLinkPluginModel
    render_template = "datacenterlight/cms/link.html"
    cache = False
    require_parent = True


@plugin_pool.register_plugin
class DCLNavbarDropdownPlugin(CMSPluginBase):
    module = "Datacenterlight"
    model = DCLNavbarDropdownPluginModel
    render_template = "datacenterlight/cms/navbar_dropdown.html"
    cache = False
    allow_children = True
    child_classes = ['DCLLinkPlugin']
    require_parent = True
    parent_classes = ['DCLNavbarPlugin']


@plugin_pool.register_plugin
class DCLContactPlugin(CMSPluginBase):
    module = "Datacenterlight"
    model = DCLContactPluginModel
    render_template = "datacenterlight/cms/contact.html"
    cache = False


@plugin_pool.register_plugin
class DCLFooterPlugin(CMSPluginBase):
    module = "Datacenterlight"
    model = DCLFooterPluginModel
    render_template = "datacenterlight/cms/footer.html"
    cache = False
    allow_children = True
    child_classes = ['DCLLinkPlugin']


@plugin_pool.register_plugin
class DCLSectionIconPlugin(CMSPluginBase):
    module = "Datacenterlight"
    model = DCLSectionIconPluginModel
    render_template = "datacenterlight/cms/section_icon.html"
    cache = False
    require_parent = True


@plugin_pool.register_plugin
class DCLSectionImagePlugin(CMSPluginBase):
    module = "Datacenterlight"
    model = DCLSectionImagePluginModel
    render_template = "datacenterlight/cms/section_image.html"
    cache = False
    require_parent = True
