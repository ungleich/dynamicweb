from django.contrib import admin
from django.utils.html import format_html
from django.core.urlresolvers import reverse

from .models import Donation


# Register your models here.


class DonationAdmin(admin.ModelAdmin):

    list_display = ('id', 'donation', 'donator')
    search_fields = ['id', 'donator__user__email']

    def user(self, obj):
        email = obj.customer.user.email
        user_url = reverse("admin:membership_customuser_change", args=[obj.customer.user.id])
        return format_html("<a href='{url}'>{email}</a>", url=user_url, email=email)


admin.site.register(Donation, DonationAdmin)
