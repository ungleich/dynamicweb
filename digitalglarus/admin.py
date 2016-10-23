from django.contrib import admin
from .models import Supporter, DGGallery, DGPicture, Booking, BookingPrice,\
    MembershipOrder, Membership, MembershipType, BookingOrder

from utils.models import ContactMessage
#
class DGPictureInline(admin.StackedInline):
    model = DGPicture

class DGGalleryAdmin(admin.ModelAdmin):
    inlines = [DGPictureInline]

admin.site.register(DGGallery, DGGalleryAdmin)
admin.site.register(ContactMessage)
admin.site.register(Booking)
admin.site.register(BookingPrice)
admin.site.register(MembershipOrder)
admin.site.register(Membership)
admin.site.register(MembershipType)
admin.site.register(BookingOrder)
