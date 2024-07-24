from django.contrib import admin
from .models import Attraction


class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    search_fields = ('name', 'region__name')


admin.site.register(Attraction, AttractionAdmin)
