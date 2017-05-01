from django.contrib import admin

from .models import Item, Bill
admin.site.register(Item)
admin.site.register(Bill)
