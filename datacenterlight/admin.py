from django.contrib import admin

from .models import BetaAccess, BetaAccessVMType, BetaAccessVM
# Register your models here.


admin.site.register(BetaAccess)
admin.site.register(BetaAccessVMType)
admin.site.register(BetaAccessVM)
