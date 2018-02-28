from djangocms_text_ckeditor.fields import HTMLField
from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.utils.safestring import mark_safe
from filer.fields.image import FilerImageField

# Models for CMS Plugins


class DCLSectionPluginModel(CMSPlugin):
    heading = models.CharField(
        blank=True, null=True, max_length=100,
        help_text='An optional heading for the Section',
    )
    content = HTMLField()
    TEXT_DIRECTIONS = (
        ('left', 'Left'),
        ('right', 'Right')
    )
    text_direction = models.CharField(
        choices=TEXT_DIRECTIONS, max_length=10, default=True,
        help_text='The alignment of text in the section'
    )


class DCLLinkPluginModel(CMSPlugin):
    target = models.CharField(
        max_length=100,
        help_text='Url or #id to navigate to'
    )
    text = models.CharField(
        max_length=50,
        help_text='Text for the menu item'
    )
    title = models.CharField(
        blank=True, null=True, max_length=100,
        help_text=(
            'Optional title text, that will be shown when a user '
            'hovers over the link'
        )
    )
    separator = models.BooleanField(
        default=False,
        help_text='Select to include a separator after the previous link'
    )


class DCLNavbarDropdownPluginModel(CMSPlugin):
    target = models.URLField(
        blank=True, null=True, max_length=100,
        help_text='Optional Url or #id to navigate on click'
    )
    text = models.CharField(
        max_length=50,
        help_text='Text for the dropdown toggle'
    )


class DCLContactPluginModel(CMSPlugin):
    heading = models.CharField(max_length=100, default="Contact", blank=True)
    organization_name = models.CharField(
        max_length=100, default="ungleich GmbH", blank=True
    )
    email = models.EmailField(max_length=200, default="info@ungleich.ch")
    address = models.CharField(
        max_length=100, default="In der Au 7, Schwanden 8762", blank=True
    )
    country = models.CharField(
        max_length=100, default="Switzerland", blank=True
    )
    form_header = models.CharField(
        max_length=100, default="Send us a message.", blank=True
    )


class DCLFooterPluginModel(CMSPlugin):
    copyright_label = models.CharField(
        max_length=100, default='ungleich GmbH', blank=True,
        help_text='Name of the company alongside the copyright year'
    )


class DCLSectionIconPluginModel(CMSPlugin):
    fontawesome_icon_name = models.CharField(
        max_length=30,
        help_text=mark_safe(
            'Name of the fontawesome icon to use. '
            '<a href="https://fontawesome.com/v4.7.0/icons/" target="_blank">'
            'Refer docs.</a>'
        )
    )


class DCLSectionImagePluginModel(CMSPlugin):
    image = FilerImageField(
        on_delete=models.CASCADE,
        help_text=(
            'Image file to be used in section. Add multiple plugins '
            'to add more than one image'
        )
    )
    caption = models.CharField(
        max_length=100, null=True, blank=True,
        help_text='Optional caption for the image.'
    )
