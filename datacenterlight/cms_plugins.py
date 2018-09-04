from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .cms_models import (
    DCLBannerItemPluginModel, DCLBannerListPluginModel, DCLContactPluginModel,
    DCLFooterPluginModel, DCLLinkPluginModel, DCLNavbarDropdownPluginModel,
    DCLSectionIconPluginModel, DCLSectionImagePluginModel,
    DCLSectionPluginModel, DCLNavbarPluginModel,
    DCLSectionPromoPluginModel, DCLCalculatorPluginModel
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
    child_classes = [
        'DCLSectionIconPlugin', 'DCLSectionImagePlugin',
        'DCLSectionPromoPlugin', 'UngleichHTMLPlugin', 'DCLCalculatorPlugin'
    ]

    def render(self, context, instance, placeholder):
        context = super(DCLSectionPlugin, self).render(
            context, instance, placeholder
        )
        context['children_to_side'] = []
        context['children_to_content'] = []
        context['children_calculator'] = []
        if instance.child_plugin_instances is not None:
            right_children = [
                'DCLSectionImagePluginModel',
                'DCLSectionIconPluginModel',
            ]
            for child in instance.child_plugin_instances:
                if child.__class__.__name__ in right_children:
                    context['children_to_side'].append(child)
                elif child.plugin_type == 'DCLCalculatorPlugin':
                    context['children_calculator'].append(child)
                else:
                    context['children_to_content'].append(child)
        return context


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
class DCLSectionPromoPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Section Promo Plugin"
    model = DCLSectionPromoPluginModel
    render_template = "datacenterlight/cms/section_promo.html"
    cache = False


@plugin_pool.register_plugin
class DCLCalculatorPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Calculator Plugin"
    model = DCLCalculatorPluginModel
    render_template = "datacenterlight/cms/calculator.html"
    cache = False
    require_parent = True

    def render(self, context, instance, placeholder):
        context = super(DCLCalculatorPlugin, self).render(
            context, instance, placeholder
        )
        ids = instance.vm_templates_to_show
        if ids:
            context['templates'] = VMTemplate.objects.filter(
                vm_type=instance.vm_type
            ).filter(opennebula_vm_template_id__in=ids)
        else:
            context['templates'] = VMTemplate.objects.filter(
                vm_type=instance.vm_type
            )
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
    model = DCLNavbarPluginModel
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
