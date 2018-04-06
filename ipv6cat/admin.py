from django.contrib import admin
from .models import Cat


# Register your models here.
class CatAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description', 'image', 'created')
    list_filter = ['created']


admin.site.register(Cat, CatAdmin)

