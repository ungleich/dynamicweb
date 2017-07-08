from django.contrib import admin
from .models import DGGallery, DGPicture, Booking, BookingPrice,\
    MembershipOrder, Membership, MembershipType, BookingOrder, BookingCancellation

from django.core.urlresolvers import reverse
from utils.models import ContactMessage
from django.utils.html import format_html


class DGPictureInline(admin.StackedInline):
    model = DGPicture


class DGGalleryAdmin(admin.ModelAdmin):
    inlines = [DGPictureInline]


class BookingCancellationAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_order', 'created_at', 'required_refund', 'refund')

    def get_order(self, obj):
        order = obj.order
        order_url = reverse("admin:digitalglarus_bookingorder_change", args=[order.id])
        return format_html("<a href='{url}'>{order_id}</a>", url=order_url, order_id=order.id)


admin.site.register(DGGallery, DGGalleryAdmin)
admin.site.register(ContactMessage)
admin.site.register(Booking)
admin.site.register(BookingPrice)
admin.site.register(MembershipOrder)
admin.site.register(Membership)
admin.site.register(MembershipType)
admin.site.register(BookingOrder)
admin.site.register(BookingCancellation, BookingCancellationAdmin)
