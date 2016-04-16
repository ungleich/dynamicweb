from django.contrib import admin
from .models import Supporter, DGGallery, DGPicture
from utils.models import ContactMessage
#
class DGPictureInline(admin.StackedInline):
    model = DGPicture

class DGGalleryAdmin(admin.ModelAdmin):
    inlines = [DGPictureInline]

admin.site.register(DGGallery, DGGalleryAdmin)
admin.site.register(ContactMessage)
admin.site.register(Supporter)