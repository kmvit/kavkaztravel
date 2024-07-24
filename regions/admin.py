from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Region


class RegionAdmin(admin.ModelAdmin):
    pass



admin.site.register(Region, RegionAdmin)
