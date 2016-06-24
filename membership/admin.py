from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.hashers import make_password


class CustomUserAdmin(admin.ModelAdmin):
    fields = ('password', 'user_permissions', 'email', 'is_admin')

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get('password')

        if not change:
            obj.validation_slug = make_password(None)

        obj.set_password(password)
        obj.save()
        return obj


admin.site.register(CustomUser, CustomUserAdmin)
